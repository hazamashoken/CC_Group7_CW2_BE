from ninja import Router

from .authsession.services import BearerTokenAuth

from .authsession import controller as auths
from .user import controller as user


app_router = Router()

app_router.add_router(
    prefix="auth/",
    router=auths.router,
    tags=["Authentications"],
)

app_router.add_router(
    prefix="/",
    router=user.router,
    tags=["Users"],
)

app_router.add_router(
    prefix="/",
    router=user.protected_router,
    auth=BearerTokenAuth(),
    tags=["Users"],
)