# Use an official Python runtime as a parent image
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY . /app

EXPOSE 8000

ENV PORT=8000

CMD uvicorn main:app --host=0.0.0.0 --port=${PORT:-8000}