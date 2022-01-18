## DOCKER-CVLoc

An auxiliary repository for the the project Image and Map Embeddings

It contains a docker-compose script to create a container with Postgres11 & Postgis2_5

The script will create 4 databases inside the container with OSM data for the following cities:
- newyork
- pittsburgh
- bristol
- london

INSTRUCTIONS

1. Install docker and docker-compose
2. Clone this repository 
3. Copy pittsburgh.osm file into postgis folder (Not provided here, but can be downloaded online)
4. Run docker-compose up
5. When container is running, initiate a shell script by using the following command
   docker exec -ti <container_id> bash
6. Run the script load_osm_data.sh inside the container to load OSM data into tables (This may take a while...)
   bash load_osm_data.sh
7. Test the container (by using getMVT.py for example, and visualizing the result in qgis) 

To check the databases do the following inside the container

1. su postgres      This will change user to postgres 
2. psql             Use psql language
3. \l               Shows all the databases
4. \c newyork       Connect to NY's database
5. \d               Shows tables in the database
6. select name from planet_osm_roads where name='Wall Street';    Do an example query
7. \q               quit database
8. exit             Exit container

Enjoy

#### Mapnik installation 

Install mapnik and dependencies. A very good tutorial to follow is 
[Installing an OpenStreetMap Tile Server on Ubuntu](https://ircama.github.io/osm-carto-tutorials/tile-server-ubuntu/ "Installing an OpenStreetMap Tile Server on Ubuntu")

#### Tested with
- Ubuntu 18.04
- Mapnik 3.0.22 (check with mapnik-config -v)
- Ensure python bindings are installed by trying to import mapnik
- Carto (check with carto -v)
- 0.18.2


#### Render map tiles for street2vec model

To render maptiles once that mapnik and mapnik-python bindings have been installed do the next

1. Clone OpenStreetMap Carto style.

    git clone --depth 1 --branch v5.1.0 https://github.com/gravitystorm/openstreetmap-carto.git

2. Edit the project.mml file from the gravitystorm directory to match the settings of the postgres database. Relevant lines are after line 32. They should look like:
- host: "localhost"
- user: "postgres"
- password: "postgres"
- dbname: "newyork"     # Adjust to the name of your database.

    **Note** If a custumized style is required modify the .mml file and its style classes defined in styles/*.mss files. Here it could be posible to remove text from map tiles but we did it modifying directly the xml file (see step 5).

3. Convert the style project_street2vec.mml file to xml using carto. The xml file should be stored in the gravitystorm directory created in the first step.

    carto -a "3.0.20" project.mml > style.xml

4. To remove all text and numbering from map tiles use the "removeTextXML" function defined in the script utils/carto.py. 

5. Go to the utils/render_tiles.py script and configure relevant lines. (save directory, zoom levels and xml style file). Then run the script.

