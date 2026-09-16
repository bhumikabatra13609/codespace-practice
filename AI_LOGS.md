You must ensure that you are sitting at the same spot where you sat in Round-1, today morning.
Round 2 is a hands-on "Builder" round that assesses how candidates approach an open-ended, real-world problem.
- Duration: The round is 2.5 hours long. Submissions will not be accepted after the 2.5-hour window closes.
- Problem statement: Each candidate will be given a short, real-world problem statement. No further explanation or specification will be provided beyond that statement.
- Deriving the solution: Candidates are expected to interpret the problem themselves and determine the features and specifications to be implemented. They are free to use any AI assistance or tools (for example, GitHub Copilot) to help infer the requirements and build their solution.
- Tech stack: Candidates may use any technology stack they are comfortable with.
- Environment: All coding is to be done online using GitHub Codespaces, accessed via the candidate's college email ID.
Chipping in for the farewell gift
The team is buying a farewell gift for their manager — budget ₹6,000. Everyone agreed to chip in equally, but in practice it’s chaos: some have paid their full share, a few paid only part, one generous soul paid extra to cover a friend, and two people haven’t paid at all. The organiser is constantly asked ‘how much do I still owe?’ and ‘have we collected enough yet?’ At the end the organiser just wants the simplest list of who should pay whom so everyone lands on their fair share.
Build something so the organiser can track the pool and settle up fairly.
(The questions the organiser keeps fielding are your clues — and build for any pool and organiser, not just this one. The easier you make it to see shares, balances and what’s left to collect, the better. Start with equal shares and simple balances, then settlements.)
give me the proper prompt to work on this and by using the github codespace
Build a complete web application called FairShare – Group Expense & Settlement Manager using Python Flask, HTML, CSS, and JavaScript.
Problem
A group of people are contributing equally toward a common expense/pool. Some people may have paid their full share, some may have paid partially, some may have paid extra, and some may not have paid anything. The organiser needs to easily see:
•	Total budget/pool amount
•	Number of participants
•	Equal share per person
•	How much each person has paid
•	How much each person still owes
•	Who has paid extra
•	Total amount collected
•	Remaining amount to collect
•	Whether the pool is fully funded
•	The simplest way to settle the final balances
The application must work for ANY group and ANY pool amount, not only the farewell-gift example.
Core Features
1. Create a Pool
Provide a form with:
•	Pool/Event name
•	Total target amount
•	Currency (default ₹)
•	Add participants
Each participant should have:
•	Name
•	Amount paid
Allow the organiser to add, edit, and remove participants.
2. Automatic Equal Share Calculation
Calculate:
Equal Share = Total Target Amount / Number of Participants
For every participant calculate:
Balance = Amount Paid - Equal Share
Interpretation:
•	Negative balance → participant still owes money
•	Positive balance → participant has paid extra and should receive money
•	Zero → participant has paid exactly their fair share
Round monetary values to 2 decimal places.
3. Dashboard
Create a clean dashboard showing summary cards:
•	Total Pool
•	Total Collected
•	Remaining to Collect
•	Equal Share
•	Participants
•	Pool Status
Pool status should clearly show:
•	Not Started
•	Partially Funded
•	Fully Funded
•	Overfunded
Also show a progress bar:
Collected / Target × 100
Do not allow the progress percentage to exceed 100%.
4. Participant Table
Display a table containing:
| Participant | Fair Share | Paid | Balance | Status |
Status examples:
•	Paid
•	Owes ₹X
•	Gets ₹X
Use clear visual indicators for positive, negative and zero balances.
5. Settlement Calculator
Create a "Settle Up" section.
The application should calculate the simplest practical set of transactions required to settle all balances.
Example:
Rahul paid ₹2500
Priya paid ₹500
Aman paid ₹1000
Neha paid ₹0
If the fair share is ₹1000:
•	Rahul should receive ₹1500
•	Priya owes ₹500
•	Aman is settled
•	Neha owes ₹1000
The application should generate transactions such as:
Neha → Rahul: ₹1000
Priya → Rahul: ₹500
Try to minimize the number of transactions.
Show the settlement list in a simple format:
Person who pays → Person who receives → Amount
6. Extra Payment Handling
If someone pays more than their fair share, treat the extra amount as money they should receive during settlement.
Example:
Fair share = ₹1000
Person pays = ₹1500
Balance = +₹500
Status = "Gets ₹500"
7. Validation
Implement useful validation:
•	Pool amount must be greater than 0
•	Participant name cannot be empty
•	Participant names should be unique
•	Paid amount cannot be negative
•	At least 1 participant is required
•	Handle decimal amounts
•	Prevent invalid form submissions
•	Handle zero participants safely
•	Display friendly error messages
8. Responsive UI
Create a professional, simple and modern interface.
The UI should include:
•	Header with application name "FairShare"
•	Dashboard summary cards
•	Add Participant form
•	Participant table
•	Settlement section
•	Clear buttons
•	Responsive layout for desktop and mobile
•	Good spacing and readable typography
Do not spend excessive time on animations. Prioritize functionality and usability.
9. Data Handling
For this assessment, use a simple Flask-based implementation.
You may use SQLite if useful, but avoid unnecessary complexity.
The application should work immediately after starting Flask.
Keep the project structure clean:
fairshare/
│
├── app.py
├── requirements.txt
├── README.md
├── templates/
│ └── index.html
├── static/
│ ├── style.css
│ └── script.js
└── database/
└── fairshare.db
10. Example Test Case
Include the following example data for testing:
Pool: Farewell Gift
Target: ₹6000
Participants:
•	Rahul: ₹2000
•	Priya: ₹500
•	Aman: ₹1500
•	Neha: ₹0
•	Karan: ₹2000
•	Simran: ₹0
The application must calculate the equal share automatically and show each person's balance.
Also test:
1.	Everyone pays equally.
2.	One person pays extra.
3.	Some people pay partially.
4.	Someone pays nothing.
5.	Pool is fully funded.
6.	Pool is overfunded.
7.	Decimal amounts.
Important Builder-Round Requirements
Do NOT create unnecessary features such as authentication, payment gateways, external APIs, deployment configuration, or complex user accounts.
Focus on making the core problem work reliably.
Before finishing:
1.	Create all required files.
2.	Install dependencies.
3.	Run the Flask application.
4.	Test the application.
5.	Fix any errors.
6.	Verify participant calculations.
7.	Verify settlement calculations.
8.	Verify the UI works correctly.
9.	Update README.md with setup and usage instructions.
If any requirement is ambiguous, make a reasonable product decision yourself and implement it rather than asking me unnecessary questions.
Start by creating the project files and implementing the application end-to-end.

How to use it in Codespaces
Once you open the GitHub Codespace:
1. Open Copilot Chat and paste the prompt above.
2. Let it create the files.
Then in the Codespace terminal run:
pip install -r requirements.txt
Then:
python app.py
If the app uses Flask's default port, open the forwarded 5000 port when Codespaces shows it.

I’ll inspect the current repository and its existing README, then establish the smallest Flask project structure around what is already there. I’ll keep calculations in integer paise, wire the browser UI to a JSON backend, and validate the core scenarios with a running app before I finish.
Created 5 todos and reviewed 2 files
Created 5 todos
Read codespace-practice
Read README.md
Ran pwd && git status --short && python3 --version
The repository is effectively empty: only a placeholder README exists, so there are no existing conventions or application state to preserve. The local hypothesis is that a small in-memory Flask API is sufficient here; the quickest check is to implement it and exercise the calculation endpoint directly, which will expose validation or settlement defects before browser work is layered on.
Updated README.md and built Flask backend+188-3
Starting: Build Flask backend and calculations (2/5)
Edited
README.md+45-1
Edited
requirements.txt+1-1
Edited
app.py+142-1
Built the complete FairShare Flask application.
Implemented:
•	Paise-safe backend calculations and validation
•	Pool dashboard with funding status and progress
•	Participant add/edit/delete/reset
•	Responsive participant table
•	Settlement algorithm
•	Farewell Gift example data

•	Frontend and backend validation
•	Professional responsive UI
•	README and requirements
Files:
•	app.py
•	index.html
•	script.js
•	style.css
•	README.md
•	requirements.txt
Validation completed:

•	Example settlement scenario
•	Fully funded, underfunded, overfunded pools
•	Decimal amounts
•	Zero contributions
•	Duplicate names
•	Negative payments
•	Syntax and editor diagnostics
The Flask server was started successfully at http://127.0.0.1:5000 and then stopped after verification. Run it again with:

Copilot generates the code and also give the proper ui. For this particular question what's the next step
Once Copilot has generated the code + UI, don't ask it to rebuild everything. Your next step should be to run, test, and validate the application against the problem statement.
Step 1 — Run the application
In the Codespaces terminal:
pip install -r requirements.txt
Then:
python app.py
If your project uses:
flask run
use that instead.
Open the forwarded port shown by Codespaces.
now, i have to use the git commands so that the code or data must be inside the codespace
Yes. In the Builder round, you should make sure your work is saved/committed to the GitHub repository from Codespaces. The safest flow is:
1. Check where you are
In the Codespaces terminal:
pwd
Then:
ls
You should see your project files, for example:
app.py
requirements.txt
templates
static
README.md
________________________________________
2. Check Git status
git status
You may see something like:
Untracked files:
    app.py
    requirements.txt
    templates/
    static/
    README.md
That's normal if Copilot just created the project.
________________________________________
3. Add all your project files
git add .
Then check:
git status
The files should now appear under Changes to be committed.
________________________________________
4. Commit the work
Use:
git commit -m "Build FairShare expense settlement application"
________________________________________
5. Push to GitHub
git push
If this is the first push and Git asks for something, show me the message rather than guessing.
________________________________________
6. Verify
Run:
git status
Ideally you'll see:
nothing to commit, working tree clean
You can also run:
git log --oneline -1
and you should see your commit.
________________________________________
If Copilot changes the code again
This is important during your assessment.
Every time you make significant changes:
git status
git add .
git commit -m "Fix settlement calculations and validation"
git push
You don't need to commit after every single line. Commit after a meaningful working milestone.
Your overall Codespaces flow
Copilot creates code
       ↓
Run application
       ↓
Test UI
       ↓
Fix bugs with Copilot
       ↓
Test again
       ↓
git status
       ↓
git add .
       ↓
git commit -m "..."
       ↓
git push
       ↓
Final GitHub repository
One important point: the Codespace itself already contains your working files, but git add → commit → push makes your work part of the Git repository and sends the commit to GitHub.
I ahve to give a file named as "REASONING.md" give me that file also 
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
