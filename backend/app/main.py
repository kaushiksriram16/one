"""HTTP API for the Campfire income statement."""
from datetime import date

from fastapi import FastAPI, HTTPException, Query

from .ledger import load_ledger
from .statement import build_income_statement

app = FastAPI(title="Income Statement API")
ledger = load_ledger()


@app.get("/income-statement")
def income_statement(
    start: date = Query(..., description="Inclusive start date, YYYY-MM-DD"),
    end: date = Query(..., description="Inclusive end date, YYYY-MM-DD"),
):
    if start > end:
        raise HTTPException(status_code=422, detail="End date must not precede start date")
    return build_income_statement(ledger, start, end)
