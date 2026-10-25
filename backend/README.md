# HireMeAI Backend

The backend is a FastAPI application API. It handles authenticated users, CVs and designs, calls the AI service, and stores uploaded files in S3-compatible storage.

## Requirements

- Python 3.12
- PostgreSQL
- MinIO or another S3-compatible object store
- The AI service for generation, tailoring, scoring, and design extraction

## Configuration

The API reads settings from environment variables and `.env` in its working directory. Set at least:

```dotenv
APP_NAME=HireMeAI API
DATABASE_URL=postgresql+psycopg://hiremeai:your-password@localhost:5432/hiremeai
CLERK_JWKS_URL=your-clerk-jwks-url
CLERK_ISSUER=your-clerk-issuer
CLERK_AUTHORIZED_PARTIES=http://localhost:3000
FRONTEND_URL=http://localhost:3000
AI_SERVICE_URL=http://localhost:8001
INTERNAL_API_SECRET=use-the-same-secret-as-the-ai-service
S3_ENDPOINT_URL=http://localhost:9000
S3_BUCKET=hiremeai-files
S3_ACCESS_KEY=your-minio-access-key
S3_SECRET_KEY=your-minio-secret-key
S3_REGION=us-east-1
MAX_UPLOAD_MB=8
```

Keep local credentials private and do not commit `.env` files.

## Run Locally

From this directory, create and activate a virtual environment, install the dependencies, apply migrations, initialize object storage, and start the API:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
python -m app.scripts.init_storage
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

On macOS or Linux, activate with `source .venv/bin/activate` and use the same remaining commands. Ensure PostgreSQL and MinIO are running and that environment variables are available to the process.

The API health endpoint is `/health`; interactive API documentation is at `/docs`.
