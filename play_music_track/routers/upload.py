from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from play_music_track.schemas.audio import AudioFormSchema
from play_music_track.services.cloudinary_services import upload_to_cloudinary
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from database import get_db
from sqlalchemy.orm import Session
from play_music_track.models.models import Audio as AudioModel

router = APIRouter()


@router.post("/upload")
async def upload_audio(
    track_name: str = Form(...),
    author_name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
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
    secure_url = await upload_to_cloudinary(file.file)

    # Step 4: Save to database
    audio_entry = AudioModel(
        url=secure_url,
        track_name=audio_data.track_name,
        author_name=audio_data.author_name,
    )
    db.add(audio_entry)
    db.commit()
    db.refresh(audio_entry)

    # Step 5: Return the data including the Cloudinary URL and saved info
    return {
        "id": audio_entry.id,
        "url": secure_url,
        "track_name": audio_entry.track_name,
        "author_name": audio_entry.author_name,
    }


@router.get("/")
def read_root():
    return RedirectResponse(url="/docs")
