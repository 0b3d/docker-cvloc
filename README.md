## DOCKER CVLoc Image

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

#### Mapnik installation 

Install mapnik and dependencies. A very good tutorial to follow is 
[Installing an OpenStreetMap Tile Server on Ubuntu](https://ircama.github.io/osm-carto-tutorials/tile-server-ubuntu/ "Installing an OpenStreetMap Tile Server on Ubuntu")




#### Requirements



#### Tested with
- Ubuntu 18.04
- Mapnik 3.0.22 (check with mapnik-config -v)
- Carto (check with carto 0.18.2)
- 0.18.2


#### Render map tiles for street2vec model

To render maptiles once that mapnik and mapnik-python bindings have been installed do the next

1. Clone OpenStreetMap's gravitystorm style.

    git clone https://github.com/gravitystorm/openstreetmap-carto.git 

2. Copy project_street2vec.mml file to the directory of gravity storm created in step 1.

3. Edit the project_street2vec.mml file from the gravitystorm directory to match the connecting settings of the postgres database. Important parameters are:
- host: 'localhost'
- user: 'postgres'
- dbname: "newyork"     # Adjust to the name of your database.

    **Note** If a custumized style is required modify the .mml file and its style classes defined in styles/*.mss files. Here it could be posible to remove text and numbering to map tiles but we did it modifying directly the xml file (see step 5).


4. Convert the style project_street2vec.mml file to xml using carto. The xml file should be stored in the gravitystorm directory created in the first step.

    carto -a "3.0.20" project_street2vec.mml > style.xml

5. To remove all text and numbering from map tiles use the "removeTextXML" function defined in the script utils/carto.py. 


6. Go to the utils/render_tiles.py script and define city (database), save directory, zoom levels and xml style file and run the script.

