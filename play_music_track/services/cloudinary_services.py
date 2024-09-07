from fastapi.responses import JSONResponse
from fastapi import status
from play_music_track.config import cloudinary
from cloudinary.uploader import upload


async def upload_to_cloudinary(file):
    try:
        cloudinary_response = cloudinary.uploader.upload(
            file,
            resource_type="auto",
        )
        secure_url = cloudinary_response.get("secure_url")
        return secure_url

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=f"Cloudinary error: {str(e)}",
        )
