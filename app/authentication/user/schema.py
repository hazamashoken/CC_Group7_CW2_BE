from ninja import Schema


class UserSchemaIn(Schema):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str


class UserSchemaOut(Schema):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
