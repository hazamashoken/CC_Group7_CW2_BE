from ninja import Router
from .models import Reservable
from .schema import ReservationSchema

router = Router()

@router.get("/", response={200: list[ReservationSchema]})
def get_reservables(request):
    reservables = Reservable.objects.all()

    return 200, reservables