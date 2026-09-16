# FairShare

FairShare is a lightweight group expense and settlement manager. It calculates each person's equal share, shows who owes or receives money, and creates a compact set of settlement transactions.

## Features

- Create a named pool with a target amount and currency symbol.
- Add, edit, and remove uniquely named participants and their contributions.
- Dashboard cards for funding, fair share, participant count, and pool status.
- Integer-paise calculations for reliable decimal money handling.
- Largest-debt-to-largest-credit settlement matching.
- Client-side and backend validation with responsive HTML/CSS/JavaScript UI.

## Technology

Python 3, Flask, HTML5, CSS3, vanilla JavaScript. No database is required; pool state is held by the browser and calculations are validated by Flask.

## Project structure

```text
fairshare/
├── app.py
├── requirements.txt
├── templates/index.html
└── static/{style.css,script.js}
```

## Install and run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Open `http://127.0.0.1:5000` in a browser.

## Settlement calculation

Fair share is `target amount / participant count`. Each balance is `paid - fair share`. Negative balances become debtors and positive balances become creditors. The API sorts both by amount descending and repeatedly transfers the smaller remaining amount, ignoring residuals below one paise.

## Example usage

The initial pool is the Farewell Gift example: target ₹6000, six participants, and a ₹1000 fair share. Rahul and Karan receive ₹1000, Aman receives ₹500, while Priya, Neha, and Simran owe ₹500, ₹1000, and ₹1000 respectively.