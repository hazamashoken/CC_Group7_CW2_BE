from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from .models import Reservation
from .schema import ReservationSchemaIn, ReservationSchemaOut

router = Router()

@router.get("/", response={200: list[ReservationSchemaOut]})
def get_reservation(request, day: int = 0):
    start_time = datetime.now() + timedelta(days=day)
    # filter to get Reservation where start_time is with in today or today + day
    reservations = Reservation.objects.filter(start_time__date=start_time.date())

    return 200, reservations

@router.get("/me/", response={200: list[ReservationSchemaOut]})
def get_reservation_by_user(request, day: int = 0):
    user = request.auth.user
    start_time = datetime.now() + timedelta(days=day)
    # filter to get Reservation where start_time is with in today or today + day
    reservations = Reservation.objects.filter(start_time__date=start_time.date(), user=user)

    return 200, reservations


@router.post("/", response={201: ReservationSchemaOut})
def post_reservation(request, payload: ReservationSchemaIn):
    user = request.auth.user

    start_time = payload.start_time
    end_time = payload.end_time

    if Reservation.objects.filter(start_time__date=start_time.date(), user=user).exists():
        raise HttpError(409, "User already has a reservation for this day")

    # check if reservable is available for that time range
    # st <= stime <= et
    # st <= etime <= et
    # stime < st < etime
    # stime < et < etime
    if Reservation.objects\
        .filter(reservable=payload.reservable, start_time__lte=start_time, end_time__gte=start_time)\
        .filter(start_time__lte=end_time, end_time__gte=end_time)\
        .filter(start_time__gt=start_time, end_time__lt=start_time)\
        .filter(end_time__gt=end_time, end_time__lt=end_time)\
        .exists():
        raise HttpError(409, "Reservable is not available at this time")

    reservation = Reservation.objects.create(**payload.dict(), user=user)

    return 201, reservation


@router.get("/{int:reservation_id}/", response={200: ReservationSchemaOut})
def get_reservation_by_id(request, reservation_id: int):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    return 200, reservation

@router.delete("/{int:reservation_id}/", response={204: None})
def delete_reservation(request, reservation_id: int):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.delete()

    return 204, None
