# FairShare – Reasoning & Design Decisions

## 1. Problem Understanding

The problem describes a group expense/pool where multiple participants are expected to contribute equally toward a common target amount.

In a real situation, participants may:

* Pay their complete share.
* Pay only part of their share.
* Pay nothing.
* Pay more than their fair share.

The organiser needs a simple way to understand the current state of the pool and determine the final payments required to settle everyone fairly.

The application is therefore designed around three main questions:

1. **How much should each person contribute?**
2. **How much has each person actually contributed?**
3. **Who needs to pay whom to settle the balances?**

---

## 2. Generalisation

The application is not limited to the farewell gift example.

The organiser can create any pool by providing:

* Pool/event name
* Target amount
* Currency
* Participants
* Amount paid by each participant

The same calculations and settlement logic are then applied to any group size and target amount.

---

## 3. Core Calculation

The application first calculates the equal share.

### Formula

```text
Fair Share = Target Amount / Number of Participants
```

For each participant, the application then calculates the balance:

```text
Balance = Amount Paid - Fair Share
```

The meaning of the balance is:

```text
Negative Balance → Participant owes money
Positive Balance → Participant should receive money
Zero Balance     → Participant is settled
```

For example, if the target is ₹6000 and there are 6 participants:

```text
Fair Share = ₹6000 / 6
           = ₹1000
```

If a participant has paid ₹500:

```text
Balance = ₹500 - ₹1000
        = -₹500
```

Therefore, the participant still owes ₹500.

If another participant has paid ₹1500:

```text
Balance = ₹1500 - ₹1000
        = +₹500
```

Therefore, that participant should receive ₹500 during settlement.

---

## 4. Pool-Level Calculations

The application separately tracks the state of the overall pool.

### Total Collected

```text
Total Collected = Sum of all participant payments
```

### Remaining Amount

For an underfunded pool:

```text
Remaining = Target Amount - Total Collected
```

The remaining amount is displayed as zero when the target has already been reached or exceeded.

### Progress

```text
Progress = (Total Collected / Target Amount) × 100
```

The displayed progress is capped at 100% so that an overfunded pool does not produce a progress bar greater than 100%.

---

## 5. Pool Status

The pool status is determined from the total collected amount.

### Not Started

Used when no money has been collected.

```text
Total Collected = 0
```

### Partially Funded

Used when:

```text
0 < Total Collected < Target Amount
```

### Fully Funded

Used when:

```text
Total Collected = Target Amount
```

### Overfunded

Used when:

```text
Total Collected > Target Amount
```

This provides the organiser with an immediate understanding of the overall collection status.

---

## 6. Why Individual Balance Is Based on Fair Share

The pool target and individual fair share represent two different concepts.

For example:

```text
Target Amount = ₹6000
Participants = 6
Fair Share = ₹1000
```

If the group has collected only ₹5000, the pool is still underfunded by ₹1000.

However, individual balances are still calculated against the ₹1000 fair share because the purpose of the balance is to determine how much each participant has contributed relative to their equal responsibility.

This separation allows the application to answer both:

* "How much more do we need to collect?"
* "Who has paid too little or too much?"

---

## 7. Settlement Approach

After calculating individual balances, participants are divided into two groups.

### Debtors

Participants with:

```text
Balance < 0
```

They need to pay money.

### Creditors

Participants with:

```text
Balance > 0
```

They need to receive money.

Participants with balances close to zero are considered settled.

---

## 8. Settlement Algorithm

To reduce unnecessary transactions, the application matches debtors and creditors.

The general process is:

1. Calculate all participant balances.
2. Create a debtor list from negative balances.
3. Create a creditor list from positive balances.
4. Sort both groups by the magnitude of their balances.
5. Match a debtor with a creditor.
6. Calculate the transferable amount as the smaller of:

   * debtor's outstanding amount
   * creditor's receivable amount
7. Create a transaction.
8. Reduce both balances by the transaction amount.
9. Remove a participant when their remaining balance reaches approximately zero.
10. Continue until all balances are settled.

Each transaction has three pieces of information:

```text
Payer
Receiver
Amount
```

The UI displays it as:

```text
Payer → Receiver : ₹Amount
```

This produces a practical settlement plan rather than requiring every participant to make payments to every other participant.

---

## 9. Example Settlement

For the example:

```text
Fair Share = ₹1000
```

Balances may be:

```text
Rahul  +₹1000
Priya  -₹500
Aman   +₹500
Neha   -₹1000
Karan  +₹1000
Simran -₹1000
```

The application identifies:

### People who should receive

```text
Rahul  ₹1000
Aman   ₹500
Karan  ₹1000
```

### People who should pay

```text
Priya  ₹500
Neha   ₹1000
Simran ₹1000
```

A valid settlement can then match these amounts, for example:

```text
Neha   → Rahul  : ₹1000
Simran → Karan  : ₹1000
Priya  → Aman   : ₹500
```

After these transactions, all individual balances are settled.

The exact transaction pairing may vary because multiple valid settlement combinations can exist.

---

# 17. Messy Contribution Import – Reasoning

Historical payment data is often copied from spreadsheets or messages, so cleaning is necessary before it can affect balances. The import uses Python's `csv` reader, trims names, collapses repeated internal whitespace, and compares normalized names case-insensitively while retaining the first clean display spelling.

Amounts are converted to integer paise after removing supported `₹`, `Rs`, `Rs.`, and `INR` prefixes and comma separators. This keeps decimal calculations reliable. Missing names, missing amounts, malformed rows, negative amounts, and values such as `abc` are rejected individually so one bad row does not block the rest of the file.

An exact duplicate is the same normalized name and amount appearing again, so only its first occurrence is counted. A merge is different: distinct valid contribution records such as `Rahul,500` and `rahul,300` belong to one normalized participant and are added together. The report shows these categories separately, including row numbers and rejected-row reasons, so the organiser can audit the import.

The API returns aggregated imported participants. The browser adds each amount to a matching existing participant, or creates one new participant when needed; it never creates a second entry for the same normalized name. The resulting participant list then follows the existing fair-share, balance, and settlement pipeline.

For example, `Rahul,1000`, `rahul,500`, and `RAHUL,500` become one Rahul participant with ₹1500 imported, while the final report identifies the last row as an exact duplicate rather than silently counting it twice.

## 10. Handling Extra Payments

An extra payment is not treated as an error.

For example:

```text
Fair Share = ₹1000
Paid       = ₹1500
```

Then:

```text
Balance = ₹1500 - ₹1000
        = +₹500
```

The participant is therefore treated as a creditor and should receive ₹500 through the settlement process.

This allows the application to handle situations where one person voluntarily pays for another participant.

---

## 11. Validation Decisions

The application validates user input to prevent incorrect calculations.

The following rules are enforced:

* Pool name cannot be empty.
* Target amount must be greater than zero.
* Participant name cannot be empty.
* Participant names must be unique.
* Paid amount cannot be negative.
* Decimal amounts are supported.
* At least one participant is required for fair-share calculation.
* Zero participants must not cause a division-by-zero error.
* Invalid numeric input should produce a friendly error rather than crashing the application.

Validation is handled as close to the user input as practical, while important calculations are also protected on the backend.

---

## 12. UI Design Reasoning

The UI is organised around the organiser's most common questions.

### Dashboard

Answers:

> "Have we collected enough?"

It displays:

* Target
* Collected
* Remaining
* Progress
* Pool status

### Participant Table

Answers:

> "Who has paid what?"

It displays:

* Fair share
* Actual payment
* Balance
* Status

### Settlement Section

Answers:

> "Who should pay whom?"

It displays the final transactions in a simple payer-to-receiver format.

The design therefore follows the natural workflow:

```text
Create Pool
    ↓
Add Participants
    ↓
Track Payments
    ↓
View Balances
    ↓
Settle Up
```

---

## 13. Technology Decisions

### Flask

Flask was selected because it is lightweight and suitable for building a small web application quickly.

It provides:

* Simple routing
* Python backend logic
* Easy integration with HTML templates
* Easy local execution

### HTML/CSS

HTML and CSS provide the application structure and responsive user interface.

### JavaScript

JavaScript is used for client-side interactions and dynamic updates where appropriate.

### SQLite

SQLite can be used for lightweight local persistence without requiring a separate database server.

No external APIs are required because the core problem is based entirely on user-provided pool and participant data.

---

## 14. Error and Edge-Case Handling

The application considers several possible edge cases:

### One Participant

The application should still calculate the fair share without crashing.

### No Participants

The application should not attempt to divide by zero.

### Everyone Settled

If all balances are zero, the settlement section should indicate that no settlement is required.

### Underfunded Pool

The organiser can see the remaining amount that must still be collected.

### Fully Funded Pool

The organiser can immediately see that the target has been reached.

### Overfunded Pool

The application shows that the target has been exceeded while still calculating individual balances using the equal-share model.

### Decimal Values

Monetary values are displayed with two decimal places.

### Floating-Point Differences

Very small calculation differences are treated as zero where appropriate so that meaningless transactions such as ₹0.00 are not generated.

---

## 15. Testing Strategy

The application should be tested using multiple scenarios rather than only the provided example.

The main test cases are:

1. Everyone pays exactly their fair share.
2. One participant pays extra.
3. One participant pays nothing.
4. Multiple participants pay partially.
5. The pool is underfunded.
6. The pool is fully funded.
7. The pool is overfunded.
8. Decimal target amounts.
9. Invalid participant data.
10. Duplicate participant names.
11. One participant.
12. Multiple debtors and creditors.
13. No settlement required.

The most important validation is that after applying all generated settlement transactions, the outstanding balances become zero or approximately zero.

---

## 16. Design Goal

The main goal of FairShare is not to create a complicated expense-management platform.

The goal is to solve the specific real-world problem with a simple flow:

```text
Track contributions
       ↓
Calculate fair shares
       ↓
Show individual balances
       ↓
Calculate remaining collection
       ↓
Generate simple settlements
```

The application therefore prioritises correctness, clarity, usability, and a practical settlement workflow over unnecessary features.
