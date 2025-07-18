from fastapi import HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import os

DB_URL = os.getenv("DATABASE_URL", "dbname=franklin user=postgres password=postgres host=db")

def get_parcel_by_id(parcel_id):
    with psycopg2.connect(DB_URL, cursor_factory=RealDictCursor) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM land_sales WHERE parcel_id = %s", (parcel_id,))
            result = cur.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Parcel not found")
            return result

def get_nearby_sales(lat, lon, radius_m):
    with psycopg2.connect(DB_URL, cursor_factory=RealDictCursor) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT * FROM land_sales
                WHERE ST_DWithin(geom, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography, %s)
            ''', (lon, lat, radius_m))
            return cur.fetchall()
