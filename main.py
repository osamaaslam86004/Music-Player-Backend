from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from play_music_track.routers import upload
from database import Base, engine

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
    expose_headers=["*"],
)


# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Include the upload module's routes
app.include_router(upload.router)
