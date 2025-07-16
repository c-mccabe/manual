from fastapi import FastAPI, File, UploadFile
import shutil
import os
import zipfile

app = FastAPI()
UPLOAD_DIR = "/mnt/data"

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

