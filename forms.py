from pydantic import BaseModel


class LoginForm(BaseModel):
    email: str
    password: str


class RegisterForm(BaseModel):
    email: str
    password: str
