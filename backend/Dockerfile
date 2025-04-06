# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY backend/ ./backend/
COPY train.py ./
COPY data/ ./data/
COPY dvc.yaml ./
COPY dvc.lock ./

# Expose port 5000 for the Flask app
EXPOSE 5000

# Command to run the prediction service
CMD ["python", "backend/main.py"]
