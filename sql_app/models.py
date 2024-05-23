
from django.template import engines
from pydantic import BaseModel, validator
from sqlalchemy import  Column, Float, Integer, String
from database import Base , engine

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    street = Column(String, index=True)
    city = Column(String, index=True)
    state = Column(String, index=True)
    postal_code = Column(String, index=True)
    country = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)

Base.metadata.create_all(bind=engine)





class AddressCreate(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    latitude: float
    longitude: float

    @validator('latitude')
    def validate_latitude(cls, v):
        if not (-90 <= v <= 90):
            raise ValueError('Latitude must be between -90 and 90')
        return v

    @validator('longitude')
    def validate_longitude(cls, v):
        if not (-180 <= v <= 180):
            raise ValueError('Longitude must be between -180 and 180')
        return v

class AddressUpdate(AddressCreate):
    pass

class AddressResponse(BaseModel):
    id: int
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    latitude: float
    longitude: float

    class Config:
        orm_mode = True

class Location(BaseModel):
    latitude: float
    longitude: float
    distance: float


