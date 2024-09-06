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
MEDIA_URL = "/media/"
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
