from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.images import HotelImagesOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import Booking
from src.schemas.facilities import Facility
from src.schemas.hotels import Hotel
from src.schemas.images import HotelImage
from src.schemas.rooms import Room, RoomsWithRels
from src.schemas.users import User


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User


class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking


class RoomsDataWithRelsMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomsWithRels


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facility


class ImageDataMapper(DataMapper):
    db_model = HotelImagesOrm
    schema = HotelImage
