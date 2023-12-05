from ninja import Router
from ninja.errors import HttpError

from .schema import (
    LoginPostIn,
    LoginPostOut,
    ValidateSessionPostOut
    )
from .services import (
    login_session,
    logout,
    BearerTokenAuth
    )
from .models import AuthSession

router = Router()


@router.post(
    "/login/",
    response={
        200: LoginPostOut,
    },
)
def post_login(request, body: LoginPostIn):
    """
    This is a function to login a user.\n
    When a user is logged in, a token is created.\n
    :param username: The username of the user.\n
    :param password: The password of the user.\n
    :return token: The token of the user.\n
    :return exp: The time when the token expires in epoch\n
    """
    session = login_session(body.username, body.password)
    if session is None:
        raise HttpError(401, "Invalid username or password")

    return 200, {"token": session.token, "exp": session.expires_at()}


@router.post(
    "/logout/",
    auth=BearerTokenAuth(),
    response={
        204: None,
    },
)
def post_logout(request):
    """
    This is a function to logout a user.\n
    When a user is logged out all the auth sessions are deleted.\n
    :param token: The token of the user.\n
    :return: True if the user is logged out.\n
    """
    user = request.auth.user

    if logout(user) is False:
        raise HttpError(401, "Invalid token")

    return 204, None


@router.get("validate-session/", response={200: ValidateSessionPostOut})
def post_validate_session(request, token):
    """
    Check if the session is valid using token.\n
    checking will not refresh session expiry time.\n.
    """
    auth_session = AuthSession.objects.filter(token=token).first()
    if auth_session is None:
        return 200, {"is_valid": False}
    if auth_session.is_expired:
        auth_session.delete()
        return 200, {"is_valid": False}
    else:
        return 200, {"is_valid": True}
