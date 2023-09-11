from cloudinary.uploader import upload
import cloudinary
from fastapi import HTTPException, status, UploadFile
from config.config import settings
import asyncio
import uuid

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

async def upload_image(files:list[UploadFile]):
    try:
        async def upload_file(file):
            file_content = await file.read()
            cloudinary_response = await asyncio.to_thread(upload, file_content)
            return cloudinary_response['secure_url']
        upload_tasks = [upload_file(file) for file in files]
        uploaded_paths = await asyncio.gather(*upload_tasks)
        return uploaded_paths
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error uploading images: {e}")

def gen_uuid() -> str:
    generated_id = uuid.uuid4()
    return generated_id.hex
