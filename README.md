# HireMeAI

HireMeAI is a CV creation and job-application assistant. It combines a web dashboard, an API for CV and design management, and an AI service for generating, tailoring, and scoring CV content.

## Project Structure

| Directory                             | Description                                                |
| ------------------------------------- | ---------------------------------------------------------- |
| [`frontend/`](frontend/README.md)     | Next.js dashboard and sign-in experience                   |
| [`backend/`](backend/README.md)       | FastAPI application API, database access, and file storage |
| [`ai-service/`](ai-service/README.md) | FastAPI service for AI-powered CV tasks                    |
| `docker-compose.yml`                  | Local PostgreSQL and MinIO services                        |

## Requirements

- Python 3.12
- Node.js 22 and pnpm 12
- Docker Compose
- Clerk credentials for authentication
- A Groq API key for AI generation; vision model credentials may also be needed for design extraction

## Local Setup

Create a root `.env` file (it is ignored by Git) and configure the values below. Use real, private credentials locally; do not commit secrets.

```dotenv
APP_ENV=development
APP_NAME=HireMeAI API
FRONTEND_URL=http://localhost:3000
POSTGRES_PASSWORD=replace-with-a-local-password
DATABASE_URL=postgresql+psycopg://hiremeai:replace-with-a-local-password@localhost:5432/hiremeai
CLERK_JWKS_URL=your-clerk-jwks-url
CLERK_ISSUER=your-clerk-issuer
CLERK_AUTHORIZED_PARTIES=http://localhost:3000
AI_SERVICE_URL=http://localhost:8001
INTERNAL_API_SECRET=replace-with-a-long-random-secret
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=your-groq-model
VISION_PROVIDER=hosted
VISION_MODEL=Qwen/Qwen2.5-VL-3B-Instruct
VISION_API_BASE_URL=
VISION_API_KEY=
MINIO_ROOT_USER=hiremeai
MINIO_ROOT_PASSWORD=replace-with-a-local-password
S3_ENDPOINT_URL=http://localhost:9000
S3_BUCKET=hiremeai-files
S3_ACCESS_KEY=hiremeai
S3_SECRET_KEY=replace-with-a-local-password
S3_REGION=us-east-1
MAX_UPLOAD_MB=8
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your-clerk-publishable-key
CLERK_SECRET_KEY=your-clerk-secret-key
```

Start the local infrastructure from the repository root:

```bash
docker compose up -d postgres minio
```

The current Compose file starts PostgreSQL and MinIO only. The backend, AI service, and frontend Compose definitions are commented out, so run those applications separately using the instructions in their READMEs. Make sure each process can read the required environment variables; the Python services load `.env` from their working directory.

## Application URLs

- Frontend: `http://localhost:3000`
- Backend API and interactive docs: `http://localhost:8000` and `http://localhost:8000/docs`
- AI service health: `http://localhost:8001/health`
- MinIO console: `http://localhost:9001`

## Security

Never commit `.env` files, API keys, signing secrets, or production credentials. Rotate any credential that has been exposed.
"# HireMeAI" 
