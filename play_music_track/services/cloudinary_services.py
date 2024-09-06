from play_music_track.config import cloudinary
from cloudinary.uploader import upload
from fastapi import HTTPException


async def upload_to_cloudinary(file):
    try:
        cloudinary_response = cloudinary.uploader.upload(
            file,
            resource_type="auto",
        )
        secure_url = cloudinary_response.get("secure_url")
        return secure_url

    except Exception as e:
        # Extract status code and details if possible from the exception
        status_code = 500  # Default to 500 if status code isn't provided
        detail = str(e)
        if hasattr(e, "response") and hasattr(e.response, "status_code"):
            status_code = e.response.status_code
        if hasattr(e, "response") and hasattr(e.response, "text"):
            detail = e.response.text

        # Raise HTTPException with the status code and details
        raise HTTPException(status_code=status_code, detail=detail)
