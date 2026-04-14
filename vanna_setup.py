import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

client = Groq(api_key=api_key)

def generate_sql(question: str, ddl_schema: str, few_shot_examples: str) -> str:
    prompt = f"""
    You are an expert SQLite developer for a clinic database.
    Database Schema:
    {ddl_schema}
    
    Example Questions and SQL:
    {few_shot_examples}
    
    User Question: {question}
    
    Rules:
    - Return ONLY the raw SQL query.
    - Do NOT use markdown formatting or backticks.
    - Do NOT include INSERT, UPDATE, DELETE, or DROP.
    """
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant", 
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    
    sql = response.choices[0].message.content.strip()
    
    
    if sql.startswith("```sql"): sql = sql[6:]
    if sql.startswith("```"): sql = sql[3:]
    if sql.endswith("```"): sql = sql[:-3]
        
    return sql.strip()