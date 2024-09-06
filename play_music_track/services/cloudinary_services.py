from play_music_track.config import cloudinary
from cloudinary.uploader import upload
from fastapi import HTTPException


async def upload_to_cloudinary(file):
    cloudinary_response = cloudinary.uploader.upload(
        file,
        resource_type="auto",
    )
    secure_url = cloudinary_response.get("secure_url")

    if not secure_url:
        raise HTTPException(
            status_code=500, detail="Failed to upload file to Cloudinary."
        )
    return secure_url
