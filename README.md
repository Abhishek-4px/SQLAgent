# NL2SQL Clinic API

A natural-language-to-SQL API built on a medical clinic SQLite database. It converts plain English questions into SQL, executes them securely, and returns JSON data along with Plotly charts.

## Architecture & Design Choices

**LLM Provider:** Groq (`llama-3.1-8b-instant`)

> **Note:** The assignment suggested using Vanna 2.0's Agent and ToolRegistry classes. However, the released PyPI package (vanna 2.0.2) contains breaking initialization bugs in these exact classes that contradict the provided documentation. To ensure the system actually worked, I mapped Vanna's intended architecture (LLM -> Validation -> Execution -> Visualization) into a clean, custom FastAPI pipeline using the native Groq SDK.

### Key Features
- **Database:** SQLite (`clinic.db`) — 5 tables: `patients`, `doctors`, `appointments`, `treatments`, `invoices`.
- **Security:** Pre-execution SQL validation (blocks DROP, INSERT, DELETE, etc.).
- **Bonus Features:** Query caching, Plotly chart generation, SlowAPI rate limiting (10 req/min), structured logging.

## Setup Instructions

1. Ensure **Python 3.10+** is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your Groq API key:
   ```text
   GROQ_API_KEY=gsk_your_key_here
   ```
   *(Get a free key at [https://console.groq.com](https://console.groq.com))*

## Running the Application

Run these commands in order:

```bash
# 1. Create the SQLite database and insert dummy data
python setup_database.py

# 2. Seed the system memory with few-shot examples
python seed_memory.py

# 3. Start the FastAPI server
uvicorn main:app --reload
```

## API Documentation

Access the interactive Swagger UI at: [http://localhost:8000/docs](http://localhost:8000/docs)

### `GET /health`
Health check to verify the API is running.

**Response:**
```json
{
  "status": "ok",
  "database": "connected",
  "agent_memory_items": 15
}
```

### `POST /chat`
Send a natural language question, receive SQL, data rows, and an optional Plotly chart JSON.

**Request Body:**
```json
{
  "question": "Show revenue by doctor"
}
```

**Response:**
```json
{
  "message": "Data retrieved successfully",
  "sql_query": "SELECT d.name, SUM(i.total_amount) ...",
  "columns": ["name", "total_revenue"],
  "rows": [{"name": "Dr. Sharma", "total_revenue": 15000}],
  "row_count": 1,
  "chart": "{ ... plotly figure json ... }"
}
```
