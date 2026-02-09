# Build
FROM python:3.12-slim AS builder

WORKDIR /app

COPY backend/requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# Prod
FROM python:3.12-slim AS prod

WORKDIR /app
ENV PYTHONPATH=/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

COPY backend/ ./backend/


# Dev
FROM python:3.12-slim AS dev

WORKDIR /app
ENV PYTHONPATH=/app/backend

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
