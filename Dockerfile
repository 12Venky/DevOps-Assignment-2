# Use slim Python base
FROM python:3.10-slim

WORKDIR /app

# install minimal system deps (kept small)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app
COPY app/ ./

EXPOSE 5000

# use gunicorn in production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "3"]
