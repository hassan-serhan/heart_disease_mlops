FROM python:3.10-slim

# Set working directory inside container
WORKDIR /heart-disease-prediction

# Install dependencies
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend and frontend
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY models/ ./models/  

# Optional: copy ML/DVC tracking configs (not used at runtime)
COPY dvc.yaml ./  
COPY dvc.lock ./  

# Set environment variables for DagsHub MLflow auth (during runtime in Render or Docker)
ENV MLFLOW_TRACKING_URI=https://dagshub.com/hassan-serhan/heartdiseaserisk11.mlflow
ENV MLFLOW_TRACKING_USERNAME=hassan-serhan
ENV MLFLOW_TRACKING_PASSWORD=f6fb42675b16121e338a1a6fa408c4f29d9185b1

# Expose the port used by Flask
EXPOSE 5000

# Run the web server (Flask in this case)
CMD ["python", "backend/app.py"]
