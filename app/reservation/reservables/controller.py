from ninja import Router
from .models import Reservable
from .schema import ReservableSchema

router = Router()

@router.get("/", response={200: list[ReservableSchema]})
def get_reservables(request):
    reservables = Reservable.objects.all()

    return 200, reservables