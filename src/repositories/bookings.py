from pydantic import BaseModel
from sqlalchemy import insert, select

from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.schemas.bookings import Booking
from src.models.rooms import RoomsOrm


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking

    async def add(self, data: BaseModel):
        get_room_price = await self.session.execute(select(RoomsOrm.price).filter_by(id=data.room_id))
        room_price = get_room_price.scalar()

        booking_add_stmt = insert(self.model).values(**data.model_dump(), price=room_price).returning(self.model)
        new_booking = await self.session.execute(booking_add_stmt)
        model = new_booking.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)
