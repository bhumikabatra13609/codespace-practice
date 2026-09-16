from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

DEFAULT_POOL = {
    "name": "Farewell Gift",
    "target": "6000",
    "currency": "₹",
    "participants": [
        {"name": "Rahul", "paid": "2000"},
        {"name": "Priya", "paid": "500"},
        {"name": "Aman", "paid": "1500"},
        {"name": "Neha", "paid": "0"},
        {"name": "Karan", "paid": "2000"},
        {"name": "Simran", "paid": "0"},
    ],
}


def money_to_paise(value, label, allow_zero=True):
    try:
        amount = Decimal(str(value).strip())
    except (InvalidOperation, ValueError, TypeError, AttributeError):
        raise ValueError(f"{label} must be a valid number.")
    if not amount.is_finite() or (not allow_zero and amount <= 0) or (allow_zero and amount < 0):
        requirement = "greater than 0" if not allow_zero else "0 or greater"
        raise ValueError(f"{label} must be {requirement}.")
    return int((amount * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def paise_to_text(value):
    return f"{Decimal(value) / 100:.2f}"


def calculate_pool(payload):
    name = str(payload.get("name", "")).strip()
    if not name:
        raise ValueError("Pool name cannot be empty.")
    target = money_to_paise(payload.get("target", ""), "Target amount", allow_zero=False)
    participants = payload.get("participants")
    if not isinstance(participants, list):
        raise ValueError("Participants must be provided as a list.")
    if len(participants) == 0:
        raise ValueError("Add at least one participant before calculating.")

    seen = set()
    parsed = []
    for participant in participants:
        if not isinstance(participant, dict):
            raise ValueError("Each participant must include a name and paid amount.")
        participant_name = str(participant.get("name", "")).strip()
        if not participant_name:
            raise ValueError("Participant names cannot be empty.")
        key = participant_name.casefold()
        if key in seen:
            raise ValueError("Participant names must be unique.")
        seen.add(key)
        paid = money_to_paise(participant.get("paid", ""), f"Paid amount for {participant_name}")
        parsed.append({"name": participant_name, "paid_paise": paid})

    fair_share = int((Decimal(target) / len(parsed)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    balances = []
    for participant in parsed:
        balance = participant["paid_paise"] - fair_share
        balances.append(balance)
        participant.update({"share_paise": fair_share, "balance_paise": balance})

    collected = sum(item["paid_paise"] for item in parsed)
    remaining = max(target - collected, 0)
    progress = min(collected / target * 100, 100)
    if collected == 0:
        status = "Not Started"
    elif collected < target:
        status = "Partially Funded"
    elif collected == target:
        status = "Fully Funded"
    else:
        status = "Overfunded"

    debtors = sorted(
        [(item["name"], -balance) for item, balance in zip(parsed, balances) if balance < -1],
        key=lambda item: item[1], reverse=True,
    )
    creditors = sorted(
        [(item["name"], balance) for item, balance in zip(parsed, balances) if balance > 1],
        key=lambda item: item[1], reverse=True,
    )
    settlements = []
    debtor_index = creditor_index = 0
    while debtor_index < len(debtors) and creditor_index < len(creditors):
        payer, debt = debtors[debtor_index]
        receiver, credit = creditors[creditor_index]
        amount = min(debt, credit)
        if amount > 0 and payer != receiver:
            settlements.append({"payer": payer, "receiver": receiver, "amount": paise_to_text(amount)})
        debtors[debtor_index] = (payer, debt - amount)
        creditors[creditor_index] = (receiver, credit - amount)
        if debt - amount <= 1:
            debtor_index += 1
        if credit - amount <= 1:
            creditor_index += 1

    return {
        "name": name,
        "target": paise_to_text(target),
        "currency": str(payload.get("currency", "₹"))[:3] or "₹",
        "total_collected": paise_to_text(collected),
        "remaining": paise_to_text(remaining),
        "fair_share": paise_to_text(fair_share),
        "progress": round(progress, 2),
        "status": status,
        "participants": [
            {"name": item["name"], "share": paise_to_text(item["share_paise"]),
             "paid": paise_to_text(item["paid_paise"]), "balance": paise_to_text(item["balance_paise"])}
            for item in parsed
        ],
        "settlements": settlements,
    }


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/example")
def example():
    return jsonify(calculate_pool(DEFAULT_POOL))


@app.post("/api/calculate")
def calculate():
    try:
        return jsonify(calculate_pool(request.get_json(silent=True) or {}))
    except ValueError as error:
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)