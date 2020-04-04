#!/bin/sh

set -e

# ------ Create all databases one by one
# Bristol
# Create the 'template_postgis' template db
psql --dbname="$DB" --user="postgres" <<- 'EOSQL'
CREATE DATABASE bristol ENCODING 'UTF-8' LC_COLLATE 'en_GB.utf8' LC_CTYPE 'en_GB.utf8' TEMPLATE template0;
CREATE EXTENSION postgis;
CREATE EXTENSION hstore;
EOSQL


# # Create databases
# for DB in bristol, london, newyork, pittsburgh; do 
# 	# Create the 'template_postgis' template db
# 	psql --dbname="$DB" --user="postgres" <<- 'EOSQL'
#     CREATE DATABASE bristol ENCODING 'UTF-8' LC_COLLATE 'en_GB.utf8' LC_CTYPE 'en_GB.utf8' TEMPLATE template0;
# 	UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'template_postgis';
# 	EOSQL
# done

# # Create extensions
# for DB in bristol, london, newyork, pittsburgh; do 
# 	echo "Loading PostGIS extensions into $DB"
# 	psql --dbname="$DB" <<-'EOSQL'
# 		CREATE EXTENSION postgis;
# 		CREATE EXTENSION hstore;
# EOSQL
# done

# echo "Loading osm to databases"
# cd openstreetmap-carto
# osm2pgsql -s -C 300 -c -G --hstore --style openstreetmap-carto.style --tag-transform-script openstreetmap-carto.lua -d Bristol -H localhost -U postgres /Bristol.osm.pbf
# osm2pgsql -s -C 300 -c -G --hstore --style openstreetmap-carto.style --tag-transform-script openstreetmap-carto.lua -d Bristol -H localhost -U postgres /London.osm.pbf
# osm2pgsql -s -C 300 -c -G --hstore --style openstreetmap-carto.style --tag-transform-script openstreetmap-carto.lua -d Bristol -H localhost -U postgres /NewYork.osm.pbf
# osm2pgsql -s -C 300 -c -G --hstore --style openstreetmap-carto.style --tag-transform-script openstreetmap-carto.lua -d Bristol -H localhost -U postgres /pittsburgh.osm.pbf

# echo "Finished"
# echo "DB successfully created, waiting for restart"
# sleep 60
# echo "Ready"