from typing import Optional

from fastapi import FastAPI , Depends , Response
from . import schemas , db , models
from .db import engine
from sqlalchemy.orm import Session 

app = FastAPI()



get_db = db.get_db
models.Base.metadata.create_all(engine)

@app.get("/")
def index():
    return {"Check": "Docs Page"}

@app.get("/addresses/")
def read_root(db : Session = Depends(get_db)):
    address = db.query(models.Address).all()
    return address

@app.post('/createaddress/',response_model=schemas.Address) 
def create_address(request: schemas.Address,db : Session = Depends(get_db)):
    new_address = models.Address(**request.dict())
    print(new_address)
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address

@app.get('/addresses/{id}', response_model=schemas.Address)
def get_address(id: int,db : Session = Depends(get_db)):
    address = db.query(models.Address).filter(models.Address.id == id).first()
    return address

@app.put('/addresses/{id}', response_model=schemas.Address)
def update_address(id: int, request: schemas.Address,db : Session = Depends(get_db)):
    address = db.query(models.Address).filter(models.Address.id == id).first()
    address.street = request.street
    address.city = request.city
    address.state = request.state
    address.zip = request.zip
    address.lat = request.lat
    address.lng = request.lng
    db.commit()
    return address

# retrieve the addresses that are within a given distance and location coordinates .
@app.get('/addresses/{lat}/{lng}/{distance}', response_model=schemas.AddressDistance)
def get_location(lat: float, lng: float, distance: int,db : Session = Depends(get_db)):
    address = db.query(models.Address).filter(models.Address.lat.between(lat-distance,lat+distance)).filter(models.Address.lng.between(lng-distance,lng+distance)).all()
    return address



