FROM python:3.11-slim

# Install system deps
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    python3-dev \
    libpq-dev \
    gcc \
    default-jre \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Create and set workdir
WORKDIR /app

# Copy only the dependency files first (for caching)
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry config virtualenvs.create false \
  && poetry install --no-root --no-interaction --no-ansi

# Copy the app code
COPY . .

EXPOSE 5000
CMD ["python", "app.py"]