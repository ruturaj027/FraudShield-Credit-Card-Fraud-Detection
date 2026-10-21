from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "creditcard.csv"

def main():
    if not DATA_PATH.is_file():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}\n"
            "Download creditcard.csv and place it in the data folder."
        )
    df = pd.read_csv(DATA_PATH)
    expected = {"Time", "Amount", "Class"}
    if not expected.issubset(df.columns):
        raise ValueError(f"Missing required columns: {sorted(expected - set(df.columns))}")
    if df.empty:
        raise ValueError("Dataset is empty.")
    if df["Class"].isna().any() or not df["Class"].isin([0, 1]).all():
        raise ValueError("Class must contain only 0 and 1 with no missing labels.")

    print("FRAUDSHIELD — DATA INSPECTION")
    print("=" * 45)
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Missing cells: {int(df.isna().sum().sum()):,}")
    print(f"Exact duplicate rows: {int(df.duplicated().sum()):,}")
    print("\nClass counts:")
    print(df["Class"].value_counts().sort_index().rename(index={0: "Genuine", 1: "Fraud"}))
    print("\nClass percentages:")
    print((df["Class"].value_counts(normalize=True).sort_index() * 100).round(4))
    print("\nAmount summary:")
    print(df["Amount"].describe().round(2))
    print("\nAmount by class:")
    print(df.groupby("Class")["Amount"].agg(["count", "mean", "median", "min", "max"]).round(2))
    print("\nInspection completed.")

if __name__ == "__main__":
    main()
