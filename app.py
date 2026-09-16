from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import csv
import io
import re
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


def normalize_name(value):
    return re.sub(r"\s+", " ", str(value or "").strip())


def parse_import_amount(value):
    cleaned = str(value or "").strip()
    cleaned = re.sub(r"^(?:₹|Rs\.?|INR)\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.replace(",", "").strip()
    if not cleaned:
        raise ValueError("Missing amount")
    return money_to_paise(cleaned, "Amount")


def import_contributions(file_bytes):
    if len(file_bytes) > 2 * 1024 * 1024:
        raise ValueError("CSV file is too large. Please use a file smaller than 2 MB.")
    try:
        text = file_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise ValueError("CSV must be a UTF-8 text file.")
    try:
        reader = csv.reader(io.StringIO(text))
        rows = list(reader)
    except csv.Error:
        raise ValueError("The CSV structure could not be read.")
    if not rows:
        raise ValueError("The CSV file is empty.")
    header = [normalize_name(value).casefold() for value in rows[0]]
    if len(header) < 2 or header[0] != "name" or header[1] != "amount":
        raise ValueError("CSV must start with the columns: name,amount")

    report = {
        "rows_received": 0, "valid_rows": 0, "duplicates_removed": 0,
        "rows_merged": 0, "rows_rejected": 0, "total_imported": "0.00",
        "rejected_rows": [], "duplicate_rows": [], "merged_names": [], "preview": [],
    }
    valid_records = []
    seen_records = {}
    merged = {}
    for row_number, row in enumerate(rows[1:], start=2):
        if not any(str(value).strip() for value in row):
            continue
        report["rows_received"] += 1
        original_name = row[0] if row else ""
        original_amount = row[1] if len(row) > 1 else ""
        if len(row) != 2:
            reason = "Expected exactly name and amount columns"
            clean_name, clean_amount = "", ""
        else:
            clean_name = normalize_name(original_name)
            try:
                amount_paise = parse_import_amount(original_amount)
                clean_amount = paise_to_text(amount_paise)
            except ValueError as error:
                amount_paise, clean_amount = None, ""
                reason = str(error).replace("Amount must be a valid number.", "Invalid amount")
            if not clean_name:
                reason = "Missing participant name"
            elif amount_paise is None:
                reason = reason if reason else "Invalid amount"
        if len(row) != 2 or not clean_name or amount_paise is None:
            report["rows_rejected"] += 1
            report["rejected_rows"].append({"row": row_number, "name": original_name.strip() if row else "", "amount": original_amount.strip() if len(row) > 1 else "", "reason": reason})
            report["preview"].append({"row": row_number, "original_name": original_name, "clean_name": clean_name, "original_amount": original_amount, "clean_amount": clean_amount or "—", "status": "Rejected"})
            continue
        name_key = clean_name.casefold()
        record_key = (name_key, amount_paise)
        if record_key in seen_records:
            report["duplicates_removed"] += 1
            report["duplicate_rows"].append({"row": row_number, "duplicate_of": seen_records[record_key]})
            report["preview"].append({"row": row_number, "original_name": original_name, "clean_name": merged.get(name_key, {"display": clean_name})["display"], "original_amount": original_amount, "clean_amount": clean_amount, "status": "Duplicate"})
            continue
        seen_records[record_key] = row_number
        report["valid_rows"] += 1
        valid_records.append((name_key, clean_name, amount_paise, original_name))
        if name_key in merged:
            report["rows_merged"] += 1
        else:
            merged[name_key] = {"display": clean_name, "variants": []}
        variant = normalize_name(original_name)
        if variant != merged[name_key]["display"] and variant not in merged[name_key]["variants"]:
            merged[name_key]["variants"].append(variant)
        report["preview"].append({"row": row_number, "original_name": original_name, "clean_name": merged[name_key]["display"], "original_amount": original_amount, "clean_amount": clean_amount, "status": "Valid"})

    aggregates = {}
    for name_key, display_name, amount_paise, _ in valid_records:
        if name_key not in aggregates:
            aggregates[name_key] = {"name": merged[name_key]["display"], "paid": 0}
        aggregates[name_key]["paid"] += amount_paise
    report["total_imported"] = paise_to_text(sum(item["paid"] for item in aggregates.values()))
    report["merged_names"] = [{"name": item["display"], "variants": item["variants"]} for item in merged.values() if item["variants"]]
    report["imported_participants"] = [{"name": item["name"], "paid": paise_to_text(item["paid"])} for item in aggregates.values()]
    return report


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


@app.post("/api/import")
def import_csv():
    uploaded = request.files.get("file")
    if not uploaded or not uploaded.filename:
        return jsonify({"error": "Choose a CSV file to import."}), 400
    if not uploaded.filename.lower().endswith(".csv"):
        return jsonify({"error": "Please choose a file with a .csv extension."}), 400
    try:
        return jsonify(import_contributions(uploaded.read()))
    except ValueError as error:
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)