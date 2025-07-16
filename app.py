from fastapi import HTTPException, FastAPI, File, UploadFile
from pydantic import BaseModel
from src.query import query_manual
from dotenv import load_dotenv

import shutil
import os
import zipfile


load_dotenv()
PERSIST_DIRECTORY = "/mnt/data/chroma_store"
app = FastAPI()
UPLOAD_DIR = "/mnt/data"


class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query_api(req: QueryRequest):
    try:
        response = query_manual(req.query, PERSIST_DIRECTORY)
        return {"answer": response["answer"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload-chroma/")
async def upload_zip(file: UploadFile = File(...)):
    zip_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save uploaded zip file to disk
    with open(zip_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Extract the zip into chroma_store directory
    extract_path = os.path.join(UPLOAD_DIR, "chroma_store")
    os.makedirs(extract_path, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    return {"status": "success", "extracted_to": extract_path}
