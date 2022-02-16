from pydantic import BaseModel


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip: str
    lat: float
    lng: float