# Use official Python base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy only requirements first (for caching)
COPY frontend/requirements.txt ./

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the frontend code
COPY frontend/ ./

# Expose Streamlit port
EXPOSE 8501

# Run the Streamlit application
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
