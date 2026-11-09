import pytest

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_q1_api_response():
    response = client.get("/income-statement", params={"start": "2026-01-01", "end": "2026-03-31"})
    assert response.status_code == 200
    body = response.json()
    assert body["company"] == "Northwind Coffee Roasters"
    assert body["currency"] == "USD"
    assert body["net_income"] == "-44480.14"
    assert len(body["sections"]["operating_expenses"]["accounts"]) == 4


def test_arbitrary_year_and_empty_period():
    response = client.get("/income-statement", params={"start": "2024-01-01", "end": "2024-12-31"})
    assert response.status_code == 200
    assert response.json()["net_income"] == "0.00"


@pytest.mark.parametrize("params", [
    {"start": "2026-04-01", "end": "2026-01-01"},
    {"start": "not-a-date", "end": "2026-03-31"},
    {"start": "2026-01-01"},
    {"end": "2026-03-31"},
])
def test_invalid_parameters(params):
    assert client.get("/income-statement", params=params).status_code == 422
