import shutil

from fastapi import UploadFile, BackgroundTasks

from src.services.base import BaseService


class ImageService(BaseService):
    @staticmethod
    def upload_image(file: UploadFile, background_tasks: BackgroundTasks, image_path: str) -> None:
        image_path = f"src/static/{image_path}"
        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)
        # resize_image.delay(image_path)
        # background_tasks.add_task(resize_image, image_path)
