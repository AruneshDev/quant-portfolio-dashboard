# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI when container runs
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
