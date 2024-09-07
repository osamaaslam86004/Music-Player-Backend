# from django.http import JsonResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from typing import List
from play_music_track.schemas.audio import AudioFormSchema, AudioResponseSchema
from play_music_track.services.cloudinary_services import upload_to_cloudinary
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from database import get_db

# from sqlalchemy.orm import Session
from play_music_track.models.models import Audio as AudioModel
import logging

logger = logging.getLogger("uvicorn")


router = APIRouter()


@router.post("/upload")
async def upload_audio(
    track_name: str = Form(...),
    author_name: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    # Step 1: Validate form data
    try:
        audio_data = AudioFormSchema(track_name=track_name, author_name=author_name)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())

    # Step 2: Check file type (ensure it's an mp3 file)
    if file.content_type not in ["audio/mpeg", "audio/mp3"]:
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only MP3 files are allowed."
        )

    # Step 4: Upload audio file to Cloudinary
    try:
        secure_url = await upload_to_cloudinary(file.file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cloudinary error: {str(e)}")

    # Step 5: Save to the database using async SQLAlchemy
    audio_entry = AudioModel(
        url=secure_url,
        track_name=audio_data.track_name,
        author_name=audio_data.author_name,
    )

    db.add(audio_entry)
    await db.commit()  # Commit the transaction (awaited)
    await db.refresh(audio_entry)  # Refresh to get the updated data (awaited)

    # Step 6: Return the data including the Cloudinary URL and saved info
    return {
        "id": audio_entry.id,
        "url": secure_url,
        "track_name": audio_entry.track_name,
        "author_name": audio_entry.author_name,
    }


@router.get("/tracks", response_model=List[AudioResponseSchema])
async def get_audio_tracks(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(AudioModel))
        tracks = result.scalars().all()
        return tracks
    except Exception as e:
        logger.error(f"Error in get_audio_tracks: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/")
def read_root():
    return RedirectResponse(url="/docs")


# @router.post("/upload")
# async def upload_audio(
#     track_name: str = Form(...),
#     author_name: str = Form(...),
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db),
# ):
#     # Step 1: Validate form data
#     try:
#         audio_data = AudioFormSchema(track_name=track_name, author_name=author_name)
#     except ValidationError as e:
#         raise HTTPException(status_code=400, detail=e.errors())

#     # Step 2: Check file type (ensure it's an mp3 file)
#     if file.content_type not in ["audio/mpeg", "audio/mp3"]:
#         raise HTTPException(
#             status_code=400, detail="Invalid file type. Only MP3 files are allowed."
#         )

#     # Step 4: Upload audio file to Cloudinary
#     try:
#         secure_url = await upload_to_cloudinary(file.file)
#     except Exception as e:
#         return JsonResponse({"status_code": e.status_code, "detail": e.detail})

#     # Step 4: Save to database
#     audio_entry = AudioModel(
#         url=secure_url,
#         track_name=audio_data.track_name,
#         author_name=audio_data.author_name,
#     )
#     db.add(audio_entry)
#     db.commit()
#     db.refresh(audio_entry)

#     # Step 5: Return the data including the Cloudinary URL and saved info
#     return {
#         "id": audio_entry.id,
#         "url": secure_url,
#         "track_name": audio_entry.track_name,
#         "author_name": audio_entry.author_name,
#     }


# @router.get("/tracks", response_model=List[AudioResponseSchema])
# async def get_audio_tracks(db: Session = Depends(get_db)):
#     tracks = db.query(AudioModel).all()
#     return tracks


# @router.get("/")
# def read_root():
#     return RedirectResponse(url="/docs")
