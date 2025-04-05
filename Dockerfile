# Base image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Install dependencies
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend and frontend
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Optional: copy ML/DVC tracking configs (not used at runtime)
COPY dvc.yaml ./
COPY dvc.lock ./

# Set environment variables for DagsHub MLflow auth (during runtime in Render or Docker)
ENV MLFLOW_TRACKING_URI=https://dagshub.com/hassan-serhan/heartdiseaserisk11.mlflow
ENV MLFLOW_TRACKING_USERNAME=${MLFLOW_TRACKING_USERNAME}
ENV MLFLOW_TRACKING_PASSWORD=${MLFLOW_TRACKING_PASSWORD}

# Expose the port used by FastAPI/Flask
EXPOSE 5000

# Run the web server (adjust depending on framework)
CMD ["python", "backend/app.py"]
