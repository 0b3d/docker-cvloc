DOCKER CVLoc Image

A docker-compose script to create a container with
    Postgres11
    Postgis2_5

The script will create 4 schemes with OSM data for the following cities:
    newyork
    pittsburgh
    bristol
    london

INSTRUCTIONS

1. Install docker and docker-compose
2. Clone this repository 
3. Copy pittsburgh.osm file into postgis folder (It is too big for github)
4. Run docker-compose up
5. When container is running, initiate a shell script by using the following command
   docker exec -ti <container_id> bash
6. Run the script load_osm_data.sh inside the container to load OSM data into tables (This may take a while...)
   bash load_osm_data.sh
7. Test the container (by using getMVT.py for example, and visualizing the result in qgis) 

Enjoy