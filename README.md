# FraudShield — Credit Card Fraud Detection

A portfolio ML engineering project that trains a baseline classifier on the public ULB/Kaggle credit-card fraud dataset and serves transaction risk estimates through a Flask web app.

## Features
- Dataset inspection and schema checks
- Leakage-conscious train/test split with stratification
- Scikit-learn preprocessing and Logistic Regression baseline
- Class weighting for imbalanced labels
- Precision, recall, F1, average precision (PR-AUC), ROC-AUC, and confusion matrix
- Flask JSON endpoint and responsive web interface
- Docker packaging and basic endpoint tests

## Dataset
Download `creditcard.csv` from https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud and place it at `data/creditcard.csv`. The CSV is excluded from Git because of size/licensing considerations. This dataset uses anonymized PCA features `V1`–`V28`, plus `Time`, `Amount`, and target `Class`.

## Windows setup
```bat
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python inspect_data.py
python train.py
python app.py
```
Open http://127.0.0.1:5000

## API
`POST /predict` accepts JSON with all 30 model input features: `Time`, `V1` through `V28`, and `Amount`. `Class` is the target and must not be provided as a feature.

Example shape:
```json
{
  "Time": 50000,
  "V1": 0,
  "V2": 0,
  "V3": 0,
  "V4": 0,
  "V5": 0,
  "V6": 0,
  "V7": 0,
  "V8": 0,
  "V9": 0,
  "V10": 0,
  "V11": 0,
  "V12": 0,
  "V13": 0,
  "V14": 0,
  "V15": 0,
  "V16": 0,
  "V17": 0,
  "V18": 0,
  "V19": 0,
  "V20": 0,
  "V21": 0,
  "V22": 0,
  "V23": 0,
  "V24": 0,
  "V25": 0,
  "V26": 0,
  "V27": 0,
  "V28": 0,
  "Amount": 75
}
```
Zero values are only a request-format example and are not a realistic or validated transaction.

## Docker
Train the model first so `models/fraud_pipeline.joblib` exists:
```bat
docker build -t fraudshield .
docker run --rm -p 5000:5000 fraudshield
```

## Engineering notes
- `class_weight="balanced"` is a baseline approach, not a guarantee of optimal performance.
- The default classification threshold is 0.5 and must be tuned on validation data based on business costs.
- Test metrics are computed on a stratified holdout. For stronger estimates, use validation/cross-validation and tune the threshold without touching the final test set.
- `Time` is a relative timestamp in this dataset; a random stratified split can overestimate future performance in some settings. Consider a time-based validation strategy for deployment-like evaluation.
- The model score is not proof of fraud. This educational demo is not connected to a bank/payment network and must not be used to make real payment decisions.
"# FraudShield-Credit-Card-Fraud-Detection" 
