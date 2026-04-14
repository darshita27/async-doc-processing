from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.orm import Session
import shutil
import os

from app.db.database import engine, Base, SessionLocal
from app.models.document import Document
from app.schemas.document import DocumentCreate
# from worker.celery_app import process_document

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/documents/")
def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).all()
# Root API
@app.get("/")
def root():
    return {"message": "Backend running with DB + Celery"}


# ✅ Create Document
@app.post("/documents/")
def create_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    new_doc = Document(name=doc.name, status="pending")
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return {
        "id": new_doc.id,
        "name": new_doc.name,
        "status": new_doc.status
    }


# ✅ Process Document
@app.post("/process/{doc_id}")
def process(doc_id: int):
    task = process_document.delay(doc_id)
    return {
        "message": "Task submitted",
        "task_id": task.id
    }


# ✅ Get Document Status
@app.get("/documents/{doc_id}")
def get_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()

    if not doc:
        return {"error": "Document not found"}

    return {
        "id": doc.id,
        "name": doc.name,
        "status": doc.status
    }


# ✅ Upload Document (FIXED POSITION)
@app.post("/upload/")
def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):

    # ✅ Ensure folder exists
    os.makedirs("uploads", exist_ok=True)

    # Save file
    file_location = f"uploads/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save to DB
    new_doc = Document(
        name=file.filename,
        file_path=file_location,
        status="pending"
    )

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    # ✅ FINAL RETURN (CORRECT)
    return {
        "id": new_doc.id,
        "name": new_doc.name,
        "status": new_doc.status,
        "result": new_doc.result
    }
