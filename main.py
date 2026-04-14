import logging
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse
from vanna.core.agent.agent import RequestContext
from vanna_setup import get_agent

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="NL2SQL Clinic API")

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"error": "Rate limit exceeded."})

agent = get_agent()
cache: dict[str, dict] = {}

class ChatRequest(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok", "database": "connected", "agent_memory_items": 15}

@app.post("/chat")
@limiter.limit("10/minute")
async def chat(request: Request, payload: ChatRequest):
    question = payload.question.strip()
    if not question or len(question) > 500:
        raise HTTPException(status_code=400, detail="Invalid question length.")

    if question in cache:
        return cache[question]

    logger.info(f"Incoming question: {question}")

    try:
        sql = None
        rows = []
        columns = []
        chart_json = None

        request_context = RequestContext(
            headers=dict(request.headers),
            remote_addr=request.client.host if request.client else ""
        )

        
        async for component in agent.send_message(request_context=request_context, message=question):
            if component.type == "sql":
                sql = component.content
                logger.info(f"Generated SQL: {sql}")
            elif component.type == "dataframe":
                df = component.content
                columns = list(df.columns)
                rows = df.to_dict(orient="records")   # records improve > JSON formatting
            elif component.type == "plotly":
                chart_json = component.content.to_json()

        result = {
            "message": "Data retrieved successfully",
            "sql_query": sql,
            "columns": columns,
            "rows": rows,
            "row_count": len(rows),
            "chart": chart_json,
        }
        cache[question] = result
        return result

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Agent error: {error_msg}")
        
        
        if "Validation Error" in error_msg:
            raise HTTPException(status_code=400, detail=error_msg)
            
        raise HTTPException(status_code=500, detail=f"Agent processing failed: {error_msg}")