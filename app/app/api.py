from ninja import NinjaAPI, Router
from reservation.api import app_router as reservation_router
from authentication.api import app_router as authentication_router

api = NinjaAPI()

api.add_router("/", reservation_router)
api.add_router("/", authentication_router)