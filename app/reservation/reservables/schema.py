from ninja import ModelSchema

from .models import Reservable


class ReservableSchemaOut(ModelSchema):
    class Config:
        model = Reservable
        model_fields = "__all__"
        
class ReservableSchemaIn(ModelSchema):
    class Config:
        model = Reservable
        model_exclude = ["id", "image", "is_active"]
        
class ReservableSchemaPatchIn(ModelSchema):
    class Config:
        model = Reservable
        model_exclude = ["id", "image", "is_active"]
        model_optional_fields = "__all__"
        