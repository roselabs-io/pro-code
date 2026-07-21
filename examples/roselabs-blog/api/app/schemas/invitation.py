from pydantic import BaseModel


class InviteCreate(BaseModel):
    email: str


class InviteAccept(BaseModel):
    token: str
    display_name: str
    password: str
