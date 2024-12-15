from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Document
from .schemas import DocumentCreate, DocumentUpdate

class DocumentCRUD:
    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(Document))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, doc_id: int):
        return await db.get(Document, doc_id)

    @staticmethod
    async def create(db: AsyncSession, document: DocumentCreate):
        new_doc = Document(**document.dict())
        db.add(new_doc)
        await db.commit()
        await db.refresh(new_doc)
        return new_doc

    @staticmethod
    async def update(db: AsyncSession, doc_id: int, document: DocumentUpdate):
        existing_doc = await db.get(Document, doc_id)
        if existing_doc:
            for key, value in document.dict().items():
                setattr(existing_doc, key, value)
            await db.commit()
            await db.refresh(existing_doc)
        return existing_doc

    @staticmethod
    async def delete(db: AsyncSession, doc_id: int):
        existing_doc = await db.get(Document, doc_id)
        if existing_doc:
            await db.delete(existing_doc)
            await db.commit()
        return existing_doc
