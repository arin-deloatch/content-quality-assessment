FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libpq-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y default-jre && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]