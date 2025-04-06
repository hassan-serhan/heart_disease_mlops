import os
import joblib
import numpy as np
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

print("Starting training script...")

# Set MLFlow tracking URI to your DagsHub MLflow server
mlflow.set_tracking_uri("https://dagshub.com/hassan-serhan/heartdiseaserisk11.mlflow")
print("MLflow tracking URI set.")

# Load the processed dataset
data_file = "data/processed/heart_processed.csv"
if not os.path.exists(data_file):
    print(f"Error: {data_file} does not exist!")
else:
    print(f"Loading data from {data_file}")
data = pd.read_csv(data_file)
print("Data loaded. Shape:", data.shape)

X = data.drop("target", axis=1)
y = data["target"]

# Split the data
print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Scale features
print("Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Set MLflow experiment
mlflow.set_experiment("Heart Disease Prediction")
print("Experiment set.")

with mlflow.start_run():
    # Define classifiers
    print("Training model...")
    clf1 = LogisticRegression(random_state=42, max_iter=1000)
    clf2 = RandomForestClassifier(random_state=42, n_estimators=100)
    gb = GradientBoostingClassifier(random_state=42)
    
    # Voting ensemble
    ensemble = VotingClassifier(
        estimators=[("lr", clf1), ("rf", clf2), ("gb", gb)],
        voting="soft"
    )
    
    # Train the model
    ensemble.fit(X_train_scaled, y_train)
    predictions = ensemble.predict(X_test_scaled)
    acc = accuracy_score(y_test, predictions)
    joblib.dump(scaler, "scaler.pkl")
   
# After training your model:
    if not os.path.exists("models"):
        os.makedirs("models")

model_path = "models/heart-disease-model.pkl"

# Save model
print(f"Saving model to {model_path}...")
joblib.dump(ensemble, model_path)

# Confirm file exists
if os.path.exists(model_path):
    print(f" Model successfully saved at {model_path}")
else:
    print(" Model save failed!")
    joblib.dump(ensemble, "models/heart-disease-model.pkl")
    mlflow.log_artifact("models/heart-disease-model.pkl", artifact_path="models")

    # print("Training complete. Accuracy:", acc)
    
    # # Log metric and model to MLflow
    # mlflow.log_metric("accuracy", acc)
    # model_info = mlflow.sklearn.log_model(ensemble, artifact_path="heart-disease-model")
    
    # # Register the model (ensure your MLflow Model Registry is properly set up on DagsHub)
    # mlflow.register_model(model_info.model_uri, "heart-disease-model")
    
    # print(f"Model registered in MLflow with accuracy: {acc}")
