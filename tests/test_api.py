
from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["model_loaded"] is True


def test_predict_returns_correct_response_format():
    payload = {
        "tenure_months": 35,
        "monthly_charges": 121.08,
        "contract": "month-to-month",
        "internet_service": "fiber",
        "support_calls": 1,
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    result = response.json()
    assert "churn_prediction" in result
    assert "churn_probability" in result


def test_predict_probability_is_valid():
    payload = {
        "tenure_months": 35,
        "monthly_charges": 121.08,
        "contract": "month-to-month",
        "internet_service": "fiber",
        "support_calls": 1,
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    result = response.json()
    assert result["churn_prediction"] in [0, 1]
    assert 0 <= result["churn_probability"] <= 1


def test_predict_rejects_missing_field():
    payload = {
        "tenure_months": 35,
        "monthly_charges": 121.08,
        "contract": "month-to-month",
        "internet_service": "fiber",
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_prediction_is_deterministic():
    payload = {
        "tenure_months": 60,
        "monthly_charges": 70.0,
        "contract": "two-year",
        "internet_service": "fiber",
        "support_calls": 0,
    }

    first_response = client.post("/predict", json=payload)
    second_response = client.post("/predict", json=payload)

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert first_response.json() == second_response.json()
