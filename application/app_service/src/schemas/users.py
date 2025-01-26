from pydantic import BaseModel, EmailStr, ConfigDict


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    password: str
    email: EmailStr


class UserCreateSchema(BaseModel):
    username: str = "likeable"
    password: str = "qwerty"
    email: EmailStr = "likeable@mail.com"


class ResultFollowerSchema(BaseModel):
    result: bool


class IDUserSchema(BaseModel):
    user_id: int
