from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    file_path = Column(String)
    status = Column(String, default="pending")
    result = Column(Text)   # ✅ NEW