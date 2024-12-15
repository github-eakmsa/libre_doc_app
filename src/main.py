from fastapi import FastAPI, HTTPException, Depends
import requests

from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db, engine
from .models import Base
from .schemas import DocumentCreate, DocumentUpdate, DocumentOut
from .crud import DocumentCRUD

app = FastAPI(title="Document Management API")

# Database initialization
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/documents/", response_model=list[DocumentOut])
async def get_documents(db: AsyncSession = Depends(get_db)):
    return await DocumentCRUD.get_all(db)

@app.get("/documents/{doc_id}", response_model=DocumentOut)
async def get_document(doc_id: int, db: AsyncSession = Depends(get_db)):
    doc = await DocumentCRUD.get_by_id(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@app.post("/documents/", response_model=DocumentOut)
async def create_document(document: DocumentCreate, db: AsyncSession = Depends(get_db)):
    
    # Get the output_path from the request
    output_path = document.file_path
    content = document.content

    try:
        # Generate the document by calling the microservice
        libreoffice_service_url = "http://127.0.0.1:5001/create_document"
        response = requests.post(
            libreoffice_service_url,
            json={
                "output_path": output_path,
                "content": content
                }
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json()
            ) 
        del document.content
        # Save metadata to the database
        metadata = await DocumentCRUD.create(db, document)
        metadata.content = ""
        return metadata
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/documents/{doc_id}", response_model=DocumentOut)
async def update_document(doc_id: int, document: DocumentUpdate, db: AsyncSession = Depends(get_db)):
    doc = await DocumentCRUD.update(db, doc_id, document)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: int, db: AsyncSession = Depends(get_db)):
    doc = await DocumentCRUD.delete(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted successfully"}
