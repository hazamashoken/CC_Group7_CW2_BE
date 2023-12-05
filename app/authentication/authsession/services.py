"""
This is a module to manage the authentication of the users.\n
# Unit test instructions
## login
login must create a token if not exist and return the token
login must refresh a token if exist and return the token
login must return None if username and password are wrong
## logout
logout must delete the token and return True
logout must return False if the token does not exist
## token_auth
token_auth must return the user if the token exist
token_auth must return None if the token does not exist
"""
from .models import AuthSession
from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractBaseUser
from ninja.security import HttpBearer


def login(username: str, password: str) -> str | None:
    """
    This is a function to login a user.\n
    When a user is logged in, a token is created for the user.\n
    :param username: The username of the user.\n
    :param password: The password of the user.\n
    :return: The token of the user.\n
    """
    user = authenticate(username=username, password=password)
    if user is not None:
        auth_session = AuthSession.objects.create(user=user)
        return str(auth_session.token)
    else:
        return None


def login_session(username: str, password: str) -> AuthSession | None :
    """
    This is a function to login a user.\n It is the same as login but instead return the session of the user.\n
    When a user is logged in, a token is created for the user.\n
    :param username: The username of the user.\n
    :param password: The password of the user.\n
    :return: The session of the user.\n
    """
    user = authenticate(username=username, password=password)
    if user is not None:
        auth_session = AuthSession.objects.create(user=user)
        return auth_session
    else:
        return None


def get_session(token: str) -> AuthSession | None:
    """
    This is a function to get the session of a user.\n
    :param token: The token of the user.\n
    :return: The session of the user.\n
    """
    try:
        auth_session = AuthSession.objects.get(token=token)
        return auth_session
    except AuthSession.DoesNotExist:
        return None


def logout(user: AbstractBaseUser) -> bool:
    """
    This is a function to logout a user.\n
    When a user is logged out, all AuthSessions are deleted.
    :param user: User\n
    :return: True if the user is logged out.\n
    """
    auth_sessions = AuthSession.objects.filter(user=user)
    auth_sessions.delete()

    return True


def token_auth(token: str) -> AuthSession | None:
    """
    This is a function to authenticate a user using a token.\n
    the token is refreshed if it is not expired.\n
    :param token: The token of the user.\n
    :return: The user.\n
    """
    try:
        auth_session = AuthSession.objects.get(token=token)
        if auth_session.is_expired:
            auth_session.delete()
            return None
        auth_session.refresh()
        auth_session.user.last_login = auth_session.last_used
        auth_session.user.save()
        return auth_session
    except AuthSession.DoesNotExist:
        return None


class BearerTokenAuth(HttpBearer):
    """
    This is a class to authenticate a user using a token.\n
    Access the auth_session request.auth.\n
    :return : The user.\n
    """

    def authenticate(self, request, token) -> AuthSession | None:
        return token_auth(token)
