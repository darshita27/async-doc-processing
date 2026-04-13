from app.db.database import SessionLocal
from app.models.document import Document
from celery import Celery

celery = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)


@celery.task
def process_document(doc_id: int):
    db = SessionLocal()

    try:
        # 1️⃣ Get document
        doc = db.query(Document).filter(Document.id == doc_id).first()

        if not doc:
            return

        # 2️⃣ Read file
        with open(doc.file_path, "r") as f:
            text = f.read()

        # 3️⃣ Count words
        word_count = len(text.split())

        # 4️⃣ Update DB
        doc.status = "completed"
        doc.result = f"File processed successfully. Word count: {word_count}"

        db.commit()

    except Exception as e:
        doc.status = "failed"
        doc.result = str(e)
        db.commit()

    finally:
        db.close()