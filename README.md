# NL2SQL Clinic — Vanna 2.0 + FastAPI

A natural-language-to-SQL API powered by Vanna 2.0 agents and Google Gemini, built on a medical clinic SQLite database.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env

```

## Running

```bash
# 1. Create the database with dummy data
python setup_database.py

# 2. Seed the agent memory with training pairs
python seed_memory.py

# 3. Start the API server
uvicorn main:app --reload
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check — returns `{"status": "ok"}` |
| `POST` | `/chat` | Send a natural language question, get SQL + results back |

### POST /chat — Request Body

```json
{
  "question": "How many appointments does each doctor have?"
}
```

### POST /chat — Response

```json
{
  "question": "How many appointments does each doctor have?",
  "sql": "SELECT ... FROM ...",
  "columns": ["doctor_name", "specialty", "appointment_count"],
  "rows": [["Dr. Sharma", "Cardiology", 12]],
  "chart": null
}
```

## Architecture

- **Database**: SQLite (`clinic.db`) — 5 tables: patients, doctors, appointments, treatments, invoices
- **Agent**: Vanna 2.0 Agent with Gemini LLM, DemoAgentMemory, and RunSqlTool
- **API**: FastAPI with rate limiting (10 req/min), SQL injection protection, and response caching
