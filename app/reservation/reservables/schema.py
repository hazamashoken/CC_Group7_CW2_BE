from ninja import ModelSchema

from .models import Reservable


class ReservableSchema(ModelSchema):
    class Config:
        model = Reservable
        model_fields = "__all__"