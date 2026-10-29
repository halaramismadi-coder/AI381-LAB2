# AI381-LAB2
## Customer Churn Prediction API

[![Churn API CI](https://github.com/halaramismadi-coder/AI381-LAB2/actions/workflows/ci.yml/badge.svg)](https://github.com/halaramismadi-coder/AI381-LAB2/actions/workflows/ci.yml)

A machine learning API that predicts whether a customer is likely to leave a service using a trained scikit-learn model.

## Technologies
- Python 3.12
- FastAPI
- scikit-learn
- Docker
- Pytest
- Ruff
- GitHub Actions
- Trivy
- GitHub Container Registry (GHCR)

## Run the Application

Build and start the API with Docker:

```bash
docker build -t churn-api . && docker run --rm -p 8000:8000 churn-api
```

Access the application:
- API: http://localhost:8000
- Interactive API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## API Endpoints

### GET /health

Checks whether the API and model are ready.

Example response:

```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### POST /predict

Predicts customer churn using customer information.

Example request:

```json
{
  "tenure_months": 35,
  "monthly_charges": 121.08,
  "contract": "month-to-month",
  "internet_service": "fiber",
  "support_calls": 1
}
```

Example response:

```json
{
  "churn_prediction": 1,
  "churn_probability": 0.6276
}
```

A prediction of `1` indicates likely churn, while `0` indicates no predicted churn.

## Run Tests

```bash
python -m pytest -v
```

## Continuous Integration and Deployment

GitHub Actions automatically runs lint checks and tests on pull requests and pushes to the main branch.

When code is pushed to main, the workflow:
1. Builds the Docker image.
2. Scans the image for vulnerabilities using Trivy.
3. Publishes the image to GitHub Container Registry.
4. Tags the image using the Git commit SHA.

## Published Docker Image

Registry: `ghcr.io/halaramismadi-coder/churn-api`

Published image tag:

`f55db3eb1ebd02174234c976a2ae68f038b48a64`

Image digest:

`sha256:e784291207cf0d30a72b46a02a4eb816003f7c7a329f524fb6901c37b054a064`

## Project Structure

```text
AI381-LAB2/
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   ├── app/
│   │   └── main.py
│   └── train/
├── tests/
│   └── test_api.py
├── Dockerfile
├── requirements.txt
├── model.joblib
├── churn_v1.csv
├── lab1_baseline.ipynb
└── README.md
```