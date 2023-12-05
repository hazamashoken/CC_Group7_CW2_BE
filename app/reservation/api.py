from ninja import Router
from .reservables import controller as reservables_controller
from .reservation import controller as reservation_controller

app_router = Router()

app_router.add_router("/reservables", reservables_controller.router, tags=["Reservables"])
app_router.add_router("/reservation", reservation_controller.router, tags=["Reservations"])