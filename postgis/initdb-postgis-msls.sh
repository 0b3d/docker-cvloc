!/bin/sh


cities=('boston' 'helsinki' 'tokyo' "toronto" "saopaulo" "moscow" "zurich" "paris" "bangkok"
              "budapest" "austin" "berlin" "ottawa" "phoenix" "goa" "amman" "nairobi" "manila" "cph" "sf")

for city in "${cities[@]}"
do 
    echo "Creating DB $city, please wait ..."
    psql --user="postgres" --host="localhost" <<- 'EOSQL'
    CREATE DATABASE $city;
    EOSQL
done

