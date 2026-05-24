from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    title: str
    description: Optional[str]=None

class PostUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str]=None


class PostResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]=None
    image_path: str
    owner_id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int