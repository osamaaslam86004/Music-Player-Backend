from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# import asyncio
import logging

# import ssl

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)  # Logs all SQL queries


DATABASE_URL = "postgresql+asyncpg://default:A9dGRnxcCk2b@ep-bold-scene-a4j046n4-pooler.us-east-1.aws.neon.tech:5432/verceldb"


# SSL context setup
# ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
# ssl_context.check_hostname = True
# ssl_context.verify_mode = ssl.CERT_REQUIRED

# Create the database engine
engine = create_async_engine(
    DATABASE_URL,
    # connect_args={"ssl": {}},  # Pass the SSL context to the connection or use default
    echo=True,
    pool_size=5,
    max_overflow=5,
    pool_timeout=360,  # Adjust timeout to wait for a connection from the pool
    pool_recycle=360,
    # poolclass = NullPoll 1. only be used in synchronous calls (db-api)
    # 2. causes opening and closing connection for every query 3. connection pooling becomes useless
)


# Create a configured "Session" class
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


# Dependency to get the database session in FastAPI routes with retry logic
async def get_db():

    try:
        async with AsyncSessionLocal() as session:
            yield session

    except OperationalError as e:
        logging.error(f"Database connection failed: {e}")


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
