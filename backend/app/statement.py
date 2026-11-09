"""Pure, exact-decimal income statement calculations."""
from datetime import date
from decimal import Decimal

ZERO = Decimal("0.00")
SECTIONS = ("revenue", "cogs", "operating_expenses", "other_income")
SUBTYPES = {
    "operating_revenue": "revenue",
    "contra_revenue": "revenue",
    "cogs": "cogs",
    "operating_expense": "operating_expenses",
    "other_income": "other_income",
}


def money(value: Decimal) -> str:
    return format(value.quantize(Decimal("0.01")), ".2f")


def build_income_statement(ledger: dict, start: date, end: date) -> dict:
    if start > end:
        raise ValueError("Start date must be on or before end date")

    accounts = {
        account["number"]: account
        for account in ledger["accounts"]
        if account["type"] in ("revenue", "expense")
        and account["subtype"] in SUBTYPES
    }
    balances = {number: ZERO for number in accounts}

    for entry in ledger["journal_entries"]:
        if entry["status"] != "posted" or not (
            start <= date.fromisoformat(entry["date"]) <= end
        ):
            continue
        for line in entry["lines"]:
            account = accounts.get(line["account"])
            if account is None:
                continue
            debit = Decimal(line["debit"])
            credit = Decimal(line["credit"])
            balances[line["account"]] += (
                credit - debit if account["type"] == "revenue"
                else debit - credit
            )

    sections = {name: {"accounts": [], "total": money(ZERO)} for name in SECTIONS}
    totals = {name: ZERO for name in SECTIONS}
    for number, account in sorted(accounts.items()):
        section = SUBTYPES[account["subtype"]]
        amount = balances[number]
        sections[section]["accounts"].append({
            "number": number, "name": account["name"], "amount": money(amount),
        })
        totals[section] += amount

    for section in SECTIONS:
        sections[section]["total"] = money(totals[section])

    gross_profit = totals["revenue"] - totals["cogs"]
    operating_income = gross_profit - totals["operating_expenses"]
    net_income = operating_income + totals["other_income"]
    return {
        "company": ledger["company"],
        "currency": ledger["currency"],
        "start": start.isoformat(),
        "end": end.isoformat(),
        "sections": sections,
        "gross_profit": money(gross_profit),
        "operating_income": money(operating_income),
        "net_income": money(net_income),
    }
