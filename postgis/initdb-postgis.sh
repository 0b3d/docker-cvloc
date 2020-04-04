!/bin/sh

#------ Create all databases one by one
psql --user="postgres" --host="localhost" <<- 'EOSQL'
CREATE DATABASE london;
CREATE DATABASE bristol;
CREATE DATABASE newyork;
CREATE DATABASE pittsburgh;
EOSQL

# Create extension in databases -------------------------------------------

# London
psql --dbname="london" --user="postgres" <<- 'EOSQL'
CREATE EXTENSION postgis;
CREATE EXTENSION hstore;
EOSQL

Bristol
psql --dbname="bristol" --user="postgres" <<- 'EOSQL'
CREATE EXTENSION postgis;
CREATE EXTENSION hstore;
EOSQL

# New York
psql --dbname="newyork" --user="postgres" <<- 'EOSQL'
CREATE EXTENSION postgis;
CREATE EXTENSION hstore;
EOSQL

# Pittsburgh
psql --dbname="pittsburgh" --user="postgres" <<- 'EOSQL'
CREATE EXTENSION postgis;
CREATE EXTENSION hstore;
EOSQL

# echo "Loading osm to databases"
cd openstreetmap-carto
osm2pgsql -s -C 300 -c -G --hstore --style openstreetmap-carto.style -d bristol -H localhost -U postgres /Bristol.osm.pbf
osm2pgsql -s -C 300 -c -G --hstore --style openstreetmap-carto.style -d london -H localhost -U postgres /London.osm.pbf
osm2pgsql -s -C 300 -c -G --hstore --style openstreetmap-carto.style -d newyork -H localhost -U postgres /NewYork.osm.pbf
osm2pgsql -s -C 300 -c -G --hstore --style openstreetmap-carto.style -d pittsburgh -H localhost -U postgres /pittsburgh.osm.pbf

cd /
echo "Finished"
echo "DB successfully created, waiting for restart"
sleep 60
echo "Ready"