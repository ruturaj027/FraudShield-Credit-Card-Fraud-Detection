# 🛡️ FraudShield — Credit Card Fraud Detection

**An ML-powered web application for detecting potentially fraudulent credit card transactions.**

FraudShield uses Machine Learning to analyze transaction details and estimate fraud risk through a professional, interactive Flask dashboard. It is designed as a beginner-friendly project demonstrating data preprocessing, model training, prediction, and web application development.

## 🚀 Features

- **Fraud Prediction:** Classifies transactions as potentially fraudulent or likely legitimate.
- **Risk Scoring:** Displays the model's estimated fraud probability when supported by the trained model.
- **Interactive Dashboard:** Professional dark UI with a fire-orange theme.
- **Transaction Analysis:** Accepts transaction amount, time, and model input features.
- **Data Analysis:** Includes tools for inspecting dataset structure and data quality.
- **Model Training:** Trains and saves a machine learning pipeline.
- **Input Validation:** Checks transaction inputs before prediction.
- **Docker Support:** Includes a Dockerfile for containerized deployment.

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Pandas & NumPy | Data processing |
| Scikit-learn | Machine learning |
| Flask | Web application and API |
| HTML & CSS | User interface |
| JavaScript | Interactive dashboard |
| Joblib | Saving and loading the trained model |
| Docker | Containerization |

## 📂 Project Structure

```text
FraudShield/
├── app.py
├── train.py
├── inspect_data.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── README.md
├── data/
│   ├── .gitkeep
│   └── creditcard.csv
├── models/
│   ├── .gitkeep
│   ├── fraud_pipeline.joblib
│   └── metrics.json
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
└── tests/
    └── test_app.py
```

*Generated model files and the dataset may be excluded from Git to keep the repository lightweight.*

## 📊 Dataset

This project is designed around the **Credit Card Fraud Detection** dataset from Kaggle.

Dataset: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

The original dataset contains anonymized transaction features, transaction time, transaction amount, and a target column named `Class`.

- `Class = 0`: Legitimate transaction
- `Class = 1`: Fraudulent transaction

**Important:** Download the dataset from Kaggle and place `creditcard.csv` inside the `data/` directory. Review the dataset's license and terms before using or redistributing it.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/FraudShield-Credit-Card-Fraud-Detection.git
cd FraudShield-Credit-Card-Fraud-Detection
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the dataset

Place the downloaded CSV file here:

```text
data/creditcard.csv
```

### 5. Train the model

```bash
python train.py
```

After successful training, the project should create the model files expected by the application, including:

```text
models/fraud_pipeline.joblib
models/metrics.json
```

### 6. Start the application

```bash
python app.py
```

Open the dashboard in your browser:

http://127.0.0.1:5000/

## 🖥️ How to Use

1. Start the Flask application.
2. Open the dashboard in your browser.
3. Enter the transaction amount and transaction time in minutes.
4. Enter the required anonymized feature values.
5. Click **Run fraud analysis**.
6. Review the predicted class and estimated risk score.

The dashboard converts the entered time from minutes to seconds before sending it to the model, matching the original dataset's `Time` feature convention.

## 🐳 Run with Docker

Build the image from the project directory:

```bash
docker build -t fraudshield .
```

Run the container:

```bash
docker run --rm -p 5000:5000 fraudshield
```

Then open:

http://127.0.0.1:5000/

**Note:** Confirm that your Dockerfile starts the Flask application on `0.0.0.0` and port `5000`. The dataset and trained model must also be available inside the container if training is not performed during the image build.

## 🔬 Machine Learning Workflow

1. Load and inspect the transaction dataset.
2. Validate the data and separate features from the target.
3. Split the data into training and testing sets.
4. Train a classification pipeline.
5. Evaluate model performance using suitable classification metrics.
6. Save the trained pipeline.
7. Load the pipeline in Flask to predict new transactions.

Because fraudulent transactions are rare, accuracy alone is not sufficient. Precision, recall, F1-score, and the confusion matrix are useful for understanding model performance.

## 🔐 Limitations and Responsible Use

- Predictions are estimates, not proof that a transaction is fraudulent or legitimate.
- The default input features are based on the dataset's anonymized variables. Real payment systems may use different features.
- A different dataset may require data cleaning, feature mapping, and model retraining before predictions are compatible.
- The application is intended for learning and demonstration, not as a production banking security system.
- Do not upload real customer card details or sensitive financial information to a public repository.

## 🔮 Future Improvements

- CSV upload and automatic dataset profiling.
- Model comparison and hyperparameter tuning.
- Interactive model evaluation charts.
- Prediction history with persistent storage.
- Authentication and role-based access.
- Production deployment with secure configuration and monitoring.

## 👨‍💻 Author

**Ruturaj Tawde**

- GitHub: https://github.com/ruturaj027
- LinkedIn: https://www.linkedin.com/in/ruturaj-tawde-a9b054292

## 📄 Disclaimer

FraudShield is an educational machine learning project. Its predictions should not be used as the sole basis for financial or security decisions.

---

⭐ If you find this project useful, consider starring the repository!
