
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "fraud_pipeline.joblib"

app = Flask(__name__)

FEATURES = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]

model = None
if MODEL_PATH.exists():
    model = joblib.load(MODEL_PATH)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/health")
def health():
    return jsonify({
        "status": "ready" if model is not None else "model_missing",
        "model_loaded": model is not None
    })


@app.route("/predict", methods=["POST"])
def predict():
    global model

    if model is None:
        return jsonify({
            "error": "Model not found. Run python train.py first."
        }), 503

    try:
        payload = request.get_json(silent=True) or {}
        row = {}

        for feature in FEATURES:
            value = payload.get(feature, 0)

            try:
                value = float(value)
            except (TypeError, ValueError):
                return jsonify({
                    "error": f"Invalid numeric value for {feature}."
                }), 400

            if not pd.notna(value):
                return jsonify({
                    "error": f"{feature} must be a finite number."
                }), 400

            row[feature] = value

        data = pd.DataFrame([row], columns=FEATURES)
        prediction = int(model.predict(data)[0])

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(data)[0]
            classes = list(model.classes_)
            fraud_index = classes.index(1) if 1 in classes else None
            fraud_probability = (
                float(probabilities[fraud_index])
                if fraud_index is not None else 0.0
            )
        else:
            fraud_probability = float(prediction)

        return jsonify({
            "prediction": prediction,
            "risk_score": round(fraud_probability * 100, 2),
            "label": "Potential Fraud" if prediction == 1
                     else "Likely Legitimate",
            "amount": row["Amount"]
        })

    except Exception:
        app.logger.exception("Prediction failed")
        return jsonify({
            "error": "Prediction failed. Check that the model and feature columns match."
        }), 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
