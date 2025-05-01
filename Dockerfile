# Use an official Python runtime as a parent image
FROM python:3.13.3-slim

# Create a working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .

# Expose the port Flask will run on (5000 by default)
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
