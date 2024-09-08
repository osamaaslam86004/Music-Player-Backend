from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from play_music_track.routers import upload
from contextlib import asynccontextmanager
from fastapi_utils.tasks import repeat_every
import logging
from database import AsyncSessionLocal

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# from database import Base, engine

app = FastAPI()


CORS_ALLOWED_ORIGINS = [
    "https://music-player-ui-ux.vercel.app",
    "http://127.0.0.1:60640",
    "https://osama11111.pythonanywhere.com",
    "https://osamaaslam.pythonanywhere.com",
    "https://web.postman.co",
    "https://diverse-intense-whippet.ngrok-free.app",
    "http://127.0.0.1:5500",
    "https://resume-builder-integrated-with-resume-api.vercel.app",
    "https://resume-builder-pwa.vercel.app/",
]


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
    # expose_headers=["*"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup task: keep database connection alive
    logger.info("Starting up and initiating keep-alive task.")

    # Define the keep-alive task
    @repeat_every(seconds=5)  # Runs every 5 seconds
    async def keep_db_alive():
        try:
            async with AsyncSessionLocal() as session:
                await session.execute("SELECT 1")
                logger.info("Keep-alive query executed successfully.")
        except Exception as e:
            logger.error(f"Error executing keep-alive query: {e}")

    # Startup tasks before yielding control to the app
    yield

    # Shutdown tasks (if any)
    logger.info("Shutting down.")
    # Cleanup tasks go here if necessary


# Set lifespan context in the FastAPI app
app = FastAPI(lifespan=lifespan)


# Sync Operation: Create all tables in the database
# Base.metadata.create_all(bind=engine)

# Include the upload module's routes
app.include_router(upload.router)
