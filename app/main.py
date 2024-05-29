from fastapi import FastAPI, HTTPException, Response, Request, status
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

@app.get("/headers")
async def return_headers(request: Request):
    my_header = request.headers.get('header-name')
    return request.headers

@app.get("/common.js")
async def get_js() :
    hdrs = {"Content-Type":"application/javascript; charset=UTF-8"}
    return Response(status_code=status.HTTP_200_OK, headers=hdrs)

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