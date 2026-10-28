from typing import List, Optional, Literal
from pydantic import BaseModel


class Category(BaseModel):
    id: int
    name: str


class Tag(BaseModel):
    id: int
    name: str


class Pet(BaseModel):
    id: int
    category: Optional[Category] = None
    name: str
    photoUrls: List[str]
    tags: List[Tag] = []
    status: Literal["available", "pending", "sold"]


class Order(BaseModel):
    id: int
    petId: int
    quantity: int
    shipDate: str
    status: Literal["placed", "approved", "delivered"]
    complete: bool


class User(BaseModel):
    id: int
    username: str
    firstName: str = ""
    lastName: str = ""
    email: str = ""
    password: str = ""
    phone: str = ""
    userStatus: int = 0
