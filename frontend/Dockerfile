# Use Python as base image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app/frontend

# Copy everything from the frontend folder into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt  

# Expose Streamlit port
EXPOSE 8501

# Start Streamlit
CMD ["streamlit", "run", "dashboard.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
