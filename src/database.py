from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine 
from sqlalchemy.orm import sessionmaker
from decouple import config  # For environment variables

# Database connection
DATABASE_URL = config("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Dependency for session
async def get_db():
    async with SessionLocal() as session:
        yield session
