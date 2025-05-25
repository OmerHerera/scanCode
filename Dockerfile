FROM python:3.11-slim

# Install zbar for pyzbar
RUN apt-get update && apt-get install -y \
    libzbar0 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy project
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable
ENV PORT=8000

# Start app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
