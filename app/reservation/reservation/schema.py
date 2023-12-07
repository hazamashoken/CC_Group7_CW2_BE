from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
import pytz
from ninja import Field, ModelSchema
from pydantic import model_validator, root_validator, validator

from reservation.reservables.models import Reservable
from .models import Reservation


utc = pytz.UTC

class ReservationSchemaOut(ModelSchema):
    class Config:
        model = Reservation
        model_fields = "__all__"
        
class ReservationSchemaIn(ModelSchema):
    start_time: datetime
    end_time: datetime
    reservable: int = Field(..., description="Reservable ID", alias="reservable_id")

    class Config:
        model = Reservation
        model_exclude = ["id", "user", "created_at", "reservable"]
        
    @validator("reservable")
    def validate_and_convert_reservable_id(cls, v):
        return get_object_or_404(Reservable, id=v)
        
    @model_validator(mode="after")
    def validate_time_range(self):
        start_time = self.start_time
        end_time =  self.end_time
        
        now = datetime.now(tz=utc)
        
        if start_time > end_time:
            raise ValueError("Start time must be before end time")
        if start_time > now + timedelta(days=2):
            raise ValueError("Cannot make reservation more than 2 days in advance")
        if start_time < now:
            raise ValueError("Start time must be in the future")
        if end_time < now:
            raise ValueError("End time must be in the future")
        if (end_time - start_time).total_seconds() > 3600:
            raise ValueError("Reservation can't be longer than 1 hour")
        if (end_time - start_time).total_seconds() < 1300:
            raise ValueError("Reservation can't be less than 30 min")

        return self
