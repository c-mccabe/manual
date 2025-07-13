from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.query import query_manual
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query_api(req: QueryRequest):
    try:
        response = query_manual(req.query)
        return {"answer": response["answer"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
