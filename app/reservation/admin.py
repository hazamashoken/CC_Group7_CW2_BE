from django.contrib import admin

from reservation.reservables.models import Reservable
from reservation.reservation.models import Reservation

# Register your models here.
admin.site.register(Reservable)
admin.site.register(Reservation)