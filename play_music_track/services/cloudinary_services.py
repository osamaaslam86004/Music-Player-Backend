from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.concurrency import run_in_threadpool
from play_music_track.config import cloudinary
import cloudinary

# Cloudinary
CLOUDINARY_CLOUD_NAME = "dh8vfw5u0"
CLOUDINARY_API_KEY = "667912285456865"
CLOUDINARY_API_SECRET = "QaF0OnEY-W1v2GufFKdOjo3KQm8"
cloudinary_url = "cloudinary://667912285456865:QaF0OnEY-W1v2GufFKdOjo3KQm8@dh8vfw5u0"


cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
)
from cloudinary.uploader import upload


async def upload_to_cloudinary(file):
    try:
        cloudinary_response = await run_in_threadpool(
            upload, file, resource_type="auto"
        )
        secure_url = cloudinary_response.get("secure_url")
        return secure_url
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=f"Cloudinary error: {str(e)}",
        )
