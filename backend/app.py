from flask import Flask, request, jsonify, render_template
from urllib.parse import quote as url_quote

import mlflow
import sys
import os
import mlflow.pyfunc
import mlflow
import mlflow.pyfunc

def load_model():
    """
    Load the latest registered version of the MLFlow model.
    """
    model_name = "heart-disease-model"
    
    # Get the latest version of the model
    latest_version = mlflow.registered_model.get_latest_versions(model_name, stages=["None"])[0].version
    model_uri = f"models:/{model_name}/{latest_version}"
    
    # Load the model
    model = mlflow.pyfunc.load_model(model_uri)
    return model


def predict_heart_disease(model, features):
    """
    Run prediction on the provided features using the given model.
    Features should be a list of values corresponding to:
    [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
    """
    prediction = model.predict([features])
    return int(prediction[0])

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

mlflow.set_tracking_uri("https://dagshub.com/hassan-serhan/heartdiseaserisk11.mlflow")

# Initialize Flask app with the correct path for the templates folder
app = Flask(__name__, template_folder='../frontend')

# Load the ML model once when the application starts.
model = load_model()

@app.route('/')
def home():
    return render_template('index.html')  # This will load the HTML file from the frontend folder

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500  # Added check for model

    try:
        # Expecting JSON payload with the following keys:
        # age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal
        data = request.get_json(force=True)
        feature_keys = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
                        'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
        features = [data.get(key) for key in feature_keys]

        # Check if any feature is missing
        if None in features:
            return jsonify({"error": "Missing one or more attributes in input data."}), 400

        # Wrap the features in the 'features' key to match MLflow's API expectation
        features_payload = {"features": [features]}  # Wrap in list (for a single prediction)

        # Run prediction using the model
        prediction = predict_heart_disease(model, features)
        return jsonify({"prediction": prediction})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
