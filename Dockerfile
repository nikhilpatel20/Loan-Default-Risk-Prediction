# ---------- BUILD STAGE ----------
FROM python:3.10-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /install

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ---------- RUNTIME STAGE ----------
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# copy python packages
COPY --from=builder /install /usr/local

# copy only required app files
COPY app/ app/

# remove caches (CRITICAL)
RUN rm -rf /root/.cache /tmp/*

EXPOSE 5000

CMD ["gunicorn", "app.app:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:5000"]

