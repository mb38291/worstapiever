from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

user_db = {}

class Address(BaseModel):
    street_address: str
    city: str
    state: str
    zip: int

class Customer(BaseModel):
    first_name: str
    last_name: str
    address: Address


app = FastAPI()

@app.get("/customers")
async def get_customer() :
    return user_db

@app.get("/customer/{id}")
async def get_customers(id: int):
    if id in user_db.keys():
        return user_db[id]
    else:
        raise HTTPException(
            status_code=404,
            detail='ID does not exist.'
        )

@app.post("/customer/{id}")
async def create_customer(id: int, customer: Customer):
    if id not in user_db.keys():
        jdata = jsonable_encoder(customer)
        user_db[id] = jdata
        return customer
    else:
        raise HTTPException(
            status_code=400,
            detail='ID already exists.'
        )