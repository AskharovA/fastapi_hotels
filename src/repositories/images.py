from src.repositories.base import BaseRepository
from src.models.images import HotelImagesOrm
from src.repositories.mappers.mappers import ImageDataMapper


class ImagesRepository(BaseRepository):
    model = HotelImagesOrm
    mapper = ImageDataMapper
