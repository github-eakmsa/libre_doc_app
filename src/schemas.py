from pydantic import BaseModel

class DocumentBase(BaseModel):
    name: str
    file_path: str
    content: str
    user: str

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(DocumentBase):
    pass

class DocumentOut(DocumentBase):
    id: str

    class Config:
        orm_mode = True
