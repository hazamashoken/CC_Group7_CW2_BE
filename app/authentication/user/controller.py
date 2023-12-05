from ninja import Router
from django.contrib.auth.models import User

from .schema import UserSchemaIn, UserSchemaOut

router = Router()

protected_router = Router()

@router.post("/register/", response={200: UserSchemaOut})
def register(request, payload: UserSchemaIn):
    """
    This is a function to register a user.\n
    :param username: The username of the user.\n
    :param password: The password of the user.\n
    :param email: The email of the user.\n
    :param first_name: The first name of the user.\n
    :param last_name: The last name of the user.\n
    :return: The user that is created.\n
    """
    user = User.objects.create_user(
        **payload.dict()
    )

    return 200, user


@protected_router.get("/me/", response={200: UserSchemaOut})
def me(request):
    """
    This is a function to get the current user.\n
    :return: The current user.\n
    """
    return 200, request.auth.user