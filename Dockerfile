FROM python:3.13-slim

WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]