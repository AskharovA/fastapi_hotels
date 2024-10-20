from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey

from src.database import Base


class HotelImagesOrm(Base):
    __tablename__ = 'hotel_images'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image_path: Mapped[str] = mapped_column(String(1000))
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
