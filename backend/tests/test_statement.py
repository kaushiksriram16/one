from datetime import date
from decimal import Decimal

import pytest

from app.ledger import load_ledger
from app.statement import build_income_statement

LEDGER = load_ledger()


def report(start: str, end: str) -> dict:
    return build_income_statement(LEDGER, date.fromisoformat(start), date.fromisoformat(end))


def amount(section: str, number: str) -> str:
    result = report("2026-01-01", "2026-03-31")
    return next(a["amount"] for a in result["sections"][section]["accounts"] if a["number"] == number)


def test_q1_totals_and_every_account():
    result = report("2026-01-01", "2026-03-31")
    assert result["sections"]["revenue"]["total"] == "37850.50"
    assert result["sections"]["cogs"]["total"] == "14272.75"
    assert result["sections"]["operating_expenses"]["total"] == "68100.07"
    assert result["sections"]["other_income"]["total"] == "42.18"
    assert result["gross_profit"] == "23577.75"
    assert result["operating_income"] == "-44522.32"
    assert result["net_income"] == "-44480.14"
    assert {number: amount(section, number) for section, number in [
        ("revenue", "4000"), ("revenue", "4100"), ("revenue", "4900"),
        ("cogs", "5000"), ("operating_expenses", "6000"),
        ("operating_expenses", "6100"), ("operating_expenses", "6200"),
        ("operating_expenses", "6300"), ("other_income", "7000")
    ]} == {
        "4000": "35650.75", "4100": "3000.00", "4900": "-800.25",
        "5000": "14272.75", "6000": "55500.00", "6100": "9000.00",
        "6200": "1099.97", "6300": "2500.10", "7000": "42.18",
    }


def test_december_2025_and_inclusive_boundaries():
    assert report("2025-12-15", "2025-12-15")["net_income"] == "5000.00"
    assert report("2025-12-16", "2025-12-31")["net_income"] == "0.00"
    assert report("2026-04-01", "2026-04-01")["net_income"] == "9100.00"


def test_zero_activity_and_unrestricted_years():
    result = report("2027-01-01", "2028-12-31")
    assert result["net_income"] == "0.00"
    assert all(section["accounts"] for section in result["sections"].values())


def test_january_rent_and_inactive_marketing():
    january = report("2026-01-01", "2026-01-31")
    assert next(a["amount"] for a in january["sections"]["operating_expenses"]["accounts"] if a["number"] == "6100") == "9000.00"
    assert next(a["amount"] for a in january["sections"]["operating_expenses"]["accounts"] if a["number"] == "6300") == "2500.10"
    february = report("2026-02-01", "2026-02-28")
    assert next(a["amount"] for a in february["sections"]["operating_expenses"]["accounts"] if a["number"] == "6100") == "0.00"


def test_void_draft_and_deferred_revenue_excluded():
    february = report("2026-02-03", "2026-02-03")
    assert february["sections"]["revenue"]["total"] == "8200.00"
    march_bonus = report("2026-03-15", "2026-03-15")
    assert march_bonus["net_income"] == "0.00"
    billing = report("2026-01-10", "2026-01-10")
    assert billing["net_income"] == "0.00"


def test_decimal_precision_and_vendor_credit():
    assert amount("operating_expenses", "6200") == "1099.97"
    assert Decimal(report("2026-01-01", "2026-03-31")["net_income"]) == Decimal("-44480.14")


def test_reversed_date_range():
    with pytest.raises(ValueError):
        report("2026-04-01", "2026-01-01")
