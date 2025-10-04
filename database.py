from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from config import DB_URL

# Create the async engine with SSL mode
engine = create_async_engine(
    DB_URL, # Pass additional arguments here
    echo=True
)

# Create the session factory
AsyncSessionFactory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Define the base class for the declarative models
Base = declarative_base()

async def get_async_session():
    async with AsyncSessionFactory() as session:
        yield session