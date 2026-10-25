FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz0b libffi-dev \
    libcairo2 libgdk-pixbuf-2.0-0 shared-mime-info && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["sh", "-c", "alembic upgrade head && attempt=0; until python -m app.scripts.init_storage; do attempt=$((attempt + 1)); if [ $attempt -ge 20 ]; then exit 1; fi; sleep 2; done; exec uvicorn app.main:app --host 0.0.0.0 --port 8000"]
