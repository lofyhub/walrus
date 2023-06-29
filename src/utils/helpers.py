from typing import List
import cloudinary.uploader
from fastapi import HTTPException, status
from config.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

async def upload_image(base64_images_list: List[str]):
    try:
        uploaded_paths = []
        for image_data in base64_images_list:
            cloudinary_response = cloudinary.uploader.upload(image_data)
            uploaded_paths.append(cloudinary_response['secure_url'])
        return uploaded_paths
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error uploading images: {e}")
