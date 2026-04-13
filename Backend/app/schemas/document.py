from pydantic import BaseModel

class DocumentCreate(BaseModel):
    name: str