# Use official Python base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Install system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libblas-dev \
    liblapack-dev \
    gfortran \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (for caching)
COPY backend/requirements.txt ./

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Manually install PyPortfolioOpt from GitHub
RUN pip install --no-cache-dir git+https://github.com/robertmartin8/PyPortfolioOpt.git

# Copy the rest of the backend code
COPY backend/ ./

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
