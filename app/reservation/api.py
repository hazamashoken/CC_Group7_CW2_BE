from ninja import Router

from authentication.authsession.services import BearerTokenAuth
from .reservables import controller as reservables_controller
from .reservation import controller as reservation_controller

app_router = Router()

app_router.add_router(
    prefix="/reservables", 
    router=reservables_controller.router, 
    auth=BearerTokenAuth(),
    tags=["Reservables"]
)

app_router.add_router(
    prefix="/reservation", 
    router=reservation_controller.router, 
    auth=BearerTokenAuth(),
    tags=["Reservations"]
)