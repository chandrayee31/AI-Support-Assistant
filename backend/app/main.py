from pathlib import Path
import shutil
from app.file_state import set_active_file, get_active_file
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.orchestrator import process_question


app = FastAPI(title="AI Support Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(__file__).parent / "uploaded_files"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class QueryRequest(BaseModel):
    question: str

class ActiveFileRequest(BaseModel):
    filename: str


@app.get("/")
def root():
    return {"message": "AI Support Assistant backend is running"}

@app.post("/set-active-file")
def set_active_uploaded_file(request: ActiveFileRequest):
    candidate = UPLOAD_DIR / request.filename

    if not candidate.exists() or not candidate.is_file():
        raise HTTPException(status_code=404, detail="File not found.")

    set_active_file(request.filename)

    return {
        "message": "Active file updated successfully.",
        "active_file": request.filename
    }


@app.post("/query")
def query(request: QueryRequest):
    answer = process_question(request.question)
    return {"answer": answer}


@app.post("/upload-sales")
def upload_sales_file(file: UploadFile = File(...)):
    allowed_extensions = {".xlsx", ".csv"}
    file_suffix = Path(file.filename).suffix.lower()

    if file_suffix not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only .xlsx and .csv files are allowed."
        )

    save_path = UPLOAD_DIR / file.filename

    try:
        with save_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        set_active_file(file.filename)

        all_files = sorted(
            [f.name for f in UPLOAD_DIR.glob("*") if f.is_file()],
            reverse=True
        )

        return {
            "message": "File uploaded successfully.",
            "filename": file.filename,
            "saved_to": str(save_path),
            "available_files": all_files,
            "active_file": file.filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
    


@app.get("/uploaded-files")
def list_uploaded_files():
    files = sorted(
        [f.name for f in UPLOAD_DIR.glob("*") if f.is_file()],
        reverse=True
    )

    active_file = get_active_file()
    if active_file is None and files:
        active_file = files[0]

    return {
        "files": files,
        "count": len(files),
        "active_file": active_file
    }