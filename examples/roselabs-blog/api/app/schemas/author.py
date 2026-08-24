import uuid

from pydantic import BaseModel, ConfigDict

from app.models.author import Role


class AuthorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    display_name: str
    role: Role
