import psycopg2 
import csv
from pyproj import Proj, transform

DATABASE = {
   'user':     'postgres',
   'host':     'localhost',
   'port':     '5432',
   'database': 'newyork'
   }

def query_buildings():
    query = """ 
        SELECT osm_id, name, building, height_to_float(tags->'height') as height, ST_X(ST_Transform(ST_Centroid(way), 4326)), ST_Y(ST_Transform(ST_Centroid(way), 4326))
        FROM planet_osm_polygon 
        WHERE building IS NOT NULL and tags->'height' IS NOT NULL;  
    """
    return query

conn = psycopg2.connect(**DATABASE)
query = query_buildings()
with conn.cursor() as cur:
    cur.execute(query)
    items = cur.fetchall()
    with open('buildings_NY.csv', mode='w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['osm_id', 'name', 'building', 'height','lon','lat'])
        for i, item in enumerate(items):
            writer.writerow(item)
            print(i,item)



