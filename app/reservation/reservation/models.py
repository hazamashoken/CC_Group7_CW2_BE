from django.db import models
from django.contrib.auth.models import User
from reservation.reservables.models import Reservable

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservable = models.ForeignKey(Reservable, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    def __str__(self):
        return self.user.username + " " + self.reservable.name + " " + str(self.start_time) + "-" + str(self.end_time)