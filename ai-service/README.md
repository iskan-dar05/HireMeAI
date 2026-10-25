# HireMeAI AI Service

This internal FastAPI service powers CV content generation, job-description tailoring, CV scoring, and visual CV-design extraction. It uses LangGraph/LangChain integrations and is intended to be called by the backend.

## Requirements

- Python 3.12
- A Groq API key and model for text-generation workflows
- A compatible vision model provider for design extraction

## Configuration

Set the following environment variables (or put them in `.env` in this directory):

```dotenv
INTERNAL_API_SECRET=use-the-same-secret-as-the-backend
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=your-groq-model
VISION_PROVIDER=hosted
VISION_MODEL=Qwen/Qwen2.5-VL-3B-Instruct
VISION_API_BASE_URL=
VISION_API_KEY=
```

The internal API secret must match the backend's `INTERNAL_API_SECRET`. Keep credentials private and do not commit `.env` files.

## Run Locally

From this directory:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

On macOS or Linux, activate with `source .venv/bin/activate` and use the same remaining commands. The service health endpoint is `/health`. Its `/internal/*` endpoints require backend authentication and should not be exposed publicly.
