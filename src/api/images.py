from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.api.dependencies import DBDep
from src.schemas.images import HotelImageAdd
from src.services.images import ImageService

router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("")
async def upload_hotel_image(hotel_id: int, file: UploadFile, background_tasks: BackgroundTasks, db: DBDep):
    image_path = f"src/static/images/{file.filename}"
    ImageService().upload_image(file, background_tasks)
    image_data = HotelImageAdd(image_path=image_path, hotel_id=hotel_id)
    await db.hotel_images.add(image_data)
    await db.commit()
