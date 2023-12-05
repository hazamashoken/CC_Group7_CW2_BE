from ninja import ModelSchema

from .models import Reservation


class ReservationSchema(ModelSchema):
    class Config:
        model = Reservation
        model_fields = "__all__"