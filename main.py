from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_sales_data, init_db
from utils import get_parcel_by_id, get_nearby_sales
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

@app.get("/sales")
def sales(query: str = "", min_price: float = 0, max_price: float = 1e9):
    return get_sales_data(query, min_price, max_price)

@app.get("/sales/{parcel_id}")
def parcel_detail(parcel_id: str):
    return get_parcel_by_id(parcel_id)

@app.get("/sales/nearby")
def sales_nearby(lat: float, lon: float, radius: int = 1000):
    return get_nearby_sales(lat, lon, radius)
