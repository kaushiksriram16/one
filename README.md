# Campfire Income Statement

Full-stack income statement for **Northwind Coffee Roasters**. Reads the unchanged Campfire ledger from `ledger.json`, calculates posted activity for any inclusive date range with Python `Decimal`, and displays account-level totals in React.

## Prerequisites
- Python **3.12+**
- Node.js **20+** and npm **10+**

These are supported target versions, not a claim about versions used to execute tests.

## Backend (macOS / Linux)
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m uvicorn app.main:app --reload
```
Backend: http://127.0.0.1:8000

## Frontend (second terminal)
```bash
cd frontend
npm install
npm run dev
```
Open the URL printed by Vite (usually http://127.0.0.1:5173). The Vite proxy forwards `/income-statement` to FastAPI.

## Tests
```bash
cd backend
python -m pytest -v
```
To check the frontend:
```bash
cd frontend
npm run build
```

## API
```http
GET /income-statement?start=2026-01-01&end=2026-03-31
```
Returns company, currency, requested period, four account-level sections with subtotals, gross profit, operating income, and net income. Amounts are exact decimal strings. Dates are inclusive; invalid dates or reversed ranges return HTTP 422.

## Usage
The page initially displays Q1 2026. Use either native calendar to select **any** start/end dates, including before 2026 or future years, and click **Generate Statement**. **Reset to Q1 2026** restores the sample dates. The JSON ledger is loaded at backend startup; restart the backend to pick up edits to `ledger.json`. An empty period returns zero amounts.

## Source
Data copied unchanged from [Campfire's take-home](https://github.com/Campfire-eng/income-statement-take-home). The application uses no database, authentication, Docker, or paid services.
