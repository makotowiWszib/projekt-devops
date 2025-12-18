FROM python:3.12-slim AS builder
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
 && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app/app


FROM builder AS test
WORKDIR /app
ENV PYTHONPATH=/app
RUN pytest -q


FROM python:3.12-slim AS final
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY --from=builder /usr/local /usr/local
COPY --from=builder /app/app /app/app

EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app.src.main:app"]
