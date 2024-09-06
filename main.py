from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from play_music_track.routers import upload
from database import Base, engine

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://music-player-ui-ux.vercel.app", "http://127.0.0.1:60640"],
    allow_credentials=False,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)


# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Include the upload module's routes
app.include_router(upload.router)
