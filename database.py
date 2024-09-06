from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://default:A9dGRnxcCk2b@ep-bold-scene-a4j046n4-pooler.us-east-1.aws.neon.tech:5432/verceldb"

# Create the database engine
engine = create_async_engine(DATABASE_URL, echo=True)

# The declarative_base() function is a synchronous operation that
# sets up a base class for all of your SQLAlchemy ORM models. This base
# class holds metadata about your models and is used to map your Python classes to database tables.


# Create a base class for your models
Base = declarative_base()

# Create a configured "Session" class
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


# Asynchronous operations in SQLAlchemy typically involve operations
# with the database engine, session, and queries, which are handled
# using the asyncpg driver and AsyncSession for non-blocking,
# asynchronous interactions with the database.


# Dependency to get the database session in FastAPI routes
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# # database.py
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # SQLite database

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


# # Dependency
# async def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
