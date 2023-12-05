
from ninja import Schema


class ValidateSessionPostOut(Schema):
    is_valid: bool


class LoginPostIn(Schema):
    username: str
    password: str


class LoginPostOut(Schema):
    token: str
    exp: int