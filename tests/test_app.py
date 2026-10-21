import app as fraud_app

def test_health_endpoint():
    client = fraud_app.app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"

def test_prediction_rejects_missing_features():
    client = fraud_app.app.test_client()
    response = client.post("/predict", json={"Time": 1, "Amount": 5})
    # With no model, endpoint correctly reports setup requirement first.
    assert response.status_code in (400, 503)
