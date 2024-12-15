from sqlalchemy import Column, String, DateTime, Integer, func
from sqlalchemy.ext.declarative import as_declarative, declared_attr
import uuid

@as_declarative()
class Base:
    id: int
    __name__: str

    # Auto-generate table names
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

class Document(Base):
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))    
    name = Column(String, nullable=True)
    file_path = Column(String, nullable=False)
    user = Column(String, nullable=True)  # Optional: store user info
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
