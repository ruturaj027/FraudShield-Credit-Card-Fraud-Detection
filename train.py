from pathlib import Path
import json
import sys
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score, classification_report, confusion_matrix,
    precision_score, recall_score, f1_score, roc_auc_score
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "creditcard.csv"
MODEL_DIR = ROOT / "models"
MODEL_PATH = MODEL_DIR / "fraud_pipeline.joblib"
METRICS_PATH = MODEL_DIR / "metrics.json"
TARGET = "Class"
FEATURES = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]

def main():
    if not DATA_PATH.is_file():
        sys.exit(f"Dataset not found: {DATA_PATH}\nDownload creditcard.csv and place it in the data folder.")

    df = pd.read_csv(DATA_PATH)
    missing = set(FEATURES + [TARGET]) - set(df.columns)
    if missing:
        sys.exit(f"Dataset is missing columns: {sorted(missing)}")
    if df.empty or df[TARGET].isna().any() or not df[TARGET].isin([0, 1]).all():
        sys.exit("Dataset is empty or the Class target is invalid.")
    if df[FEATURES].isna().any().any():
        print("Warning: input features contain missing values; median imputation will be fitted on training data.")
    if not np.isfinite(df[FEATURES].select_dtypes(include=np.number).to_numpy()).all():
        sys.exit("Dataset contains infinite or non-numeric feature values.")

    X = df[FEATURES].copy()
    y = df[TARGET].astype(int)
    if y.nunique() != 2:
        sys.exit("Training requires both class 0 and class 1.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    preprocessor = ColumnTransformer([
        ("numeric", numeric_pipeline, FEATURES)
    ])
    pipeline = Pipeline([
        ("preprocess", preprocessor),
        ("classifier", LogisticRegression(
            class_weight="balanced", max_iter=2000, random_state=42
        ))
    ])

    print("Training Logistic Regression baseline...")
    pipeline.fit(X_train, y_train)
    probabilities = pipeline.predict_proba(X_test)[:, 1]
    threshold = 0.5
    predictions = (probabilities >= threshold).astype(int)

    metrics = {
        "model": "LogisticRegression(class_weight='balanced')",
        "threshold": threshold,
        "test_rows": int(len(y_test)),
        "fraud_rows_test": int(y_test.sum()),
        "precision": float(precision_score(y_test, predictions, zero_division=0)),
        "recall": float(recall_score(y_test, predictions, zero_division=0)),
        "f1": float(f1_score(y_test, predictions, zero_division=0)),
        "average_precision_pr_auc": float(average_precision_score(y_test, probabilities)),
        "roc_auc": float(roc_auc_score(y_test, probabilities)),
        "confusion_matrix_labels_0_1": confusion_matrix(y_test, predictions, labels=[0, 1]).tolist(),
        "classification_report": classification_report(
            y_test, predictions, labels=[0, 1],
            target_names=["legitimate", "fraud"], output_dict=True, zero_division=0
        )
    }

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    print("\nEvaluation on held-out test set (threshold=0.5)")
    print(classification_report(y_test, predictions, target_names=["legitimate", "fraud"], zero_division=0))
    print("Confusion matrix [ [TN, FP], [FN, TP] ]:")
    print(confusion_matrix(y_test, predictions, labels=[0, 1]))
    print(f"PR-AUC / Average Precision: {metrics['average_precision_pr_auc']:.4f}")
    print(f"ROC-AUC: {metrics['roc_auc']:.4f}")
    print(f"\nSaved model: {MODEL_PATH}")
    print(f"Saved metrics: {METRICS_PATH}")
    print("Note: this is a baseline model. Tune threshold on validation data before operational use.")

if __name__ == "__main__":
    main()
