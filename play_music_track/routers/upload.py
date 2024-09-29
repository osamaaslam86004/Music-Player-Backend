import logging
from fastapi.routing import APIRouter

logger = logging.getLogger("uvicorn")


router = APIRouter()


@router.get("/")
def read_root():
    return RedirectResponse(url="/docs")


@router.options("/upload/")
async def options_upload():
    return JSONResponse(
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        },
        content=None,
    )


# ----------------------- for psycopg3 -------------------------------
from fastapi import APIRouter, File, UploadFile, Form, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from play_music_track.schemas.audio import AudioFormSchema, AudioResponseSchema
from play_music_track.services.cloudinary_services import upload_to_cloudinary
from pydantic import ValidationError
from database import get_db
from play_music_track.models.models import Audio
from sqlalchemy.future import select

router = APIRouter()


@router.post("/upload/", response_model=AudioResponseSchema)
async def upload_audio(
    track_name: str = Form(...),
    author_name: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    try:
        audio_data = AudioFormSchema(track_name=track_name, author_name=author_name)
    except ValidationError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=e.errors(),
        )

    if file.content_type not in ["audio/mpeg", "audio/mp3"]:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content="Invalid file type. Only MP3 files are allowed.",
        )

    secure_url = await upload_to_cloudinary(file.file)

    # Insert into PostgreSQL using SQLAlchemy ORM
    new_audio = Audio(track_name=track_name, author_name=author_name, url=secure_url)

    db.add(new_audio)
    await db.commit()
    await db.refresh(new_audio)

    return AudioResponseSchema(
        id=new_audio.id,
        track_name=new_audio.track_name,
        author_name=new_audio.author_name,
        url=new_audio.url,
    )


@router.get("/tracks/", response_model=List[AudioResponseSchema])
async def get_audio_tracks(db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(Audio))
    tracks = query.scalars().all()

    return [
        AudioResponseSchema(
            id=track.id,
            track_name=track.track_name,
            author_name=track.author_name,
            url=track.url,
        )
        for track in tracks
    ]


# ---------------- for asyncpg  + sqlachemy-------------------------------


# from sqlalchemy.exc import OperationalError
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from fastapi import APIRouter, File, UploadFile, Form, Depends, status
# from fastapi.responses import JSONResponse
# from typing import List
# from play_music_track.schemas.audio import AudioFormSchema, AudioResponseSchema
# from play_music_track.services.cloudinary_services import upload_to_cloudinary
from fastapi.responses import RedirectResponse

# from pydantic import ValidationError
# from database import get_db
# from play_music_track.models.models import Audio as AudioModel


# @router.post("/upload/")
# async def upload_audio(
#     track_name: str = Form(...),
#     author_name: str = Form(...),
#     file: UploadFile = File(...),
#     db: AsyncSession = Depends(get_db),
# ):
#     try:
#         audio_data = AudioFormSchema(track_name=track_name, author_name=author_name)
#     except ValidationError as e:
#         return JSONResponse(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             content=e.errors(),
#         )

#     if file.content_type not in ["audio/mpeg", "audio/mp3"]:
#         return JSONResponse(
#             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             content="Invalid file type. Only MP3 files are allowed.",
#         )

#     secure_url = await upload_to_cloudinary(file.file)

#     try:
#         audio_entry = AudioModel(
#             url=secure_url,
#             track_name=audio_data.track_name,
#             author_name=audio_data.author_name,
#         )
#         db.add(audio_entry)
#         try:
#             await db.commit()
#         except Exception as e:
#             logging.error(f"Failed to commit to the database: {e}")
#             await db.rollback()  # Rollback the transaction in case of failure
#             raise  # Re-raise the exception for debugging

#         await db.refresh(audio_entry)

#         return {
#             "id": audio_entry.id,
#             "url": secure_url,
#             "track_name": audio_entry.track_name,
#             "author_name": audio_entry.author_name,
#         }

#     except OperationalError as e:
#         logging.error(f"Database connection failed: {e}")

#         return JSONResponse(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             content=str(e),
#         )


# @router.get("/tracks/", response_model=List[AudioResponseSchema])
# async def get_audio_tracks(db: AsyncSession = Depends(get_db)):
#     try:
#         result = await db.execute(select(AudioModel))
#         tracks = result.scalars().all()
#         return tracks

#     except OperationalError as e:
#         logger.error(f"Connection to database lost: {e}")
#         return JSONResponse(
#             status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#             content="Database Connection Lost",
#         )

#     except Exception as e:
#         logger.error(f"Error in get_audio_tracks: {e}")
#         return JSONResponse(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             content=f"{e}",
#         )
