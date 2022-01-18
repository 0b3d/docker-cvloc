FROM mdillon/postgis:11

WORKDIR /

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y osm2pgsql osmctools git wget 

RUN rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 --branch v5.1.0 https://github.com/gravitystorm/openstreetmap-carto.git && \
    wget https://download.bbbike.org/osm/bbbike/Bristol/Bristol.osm.pbf && \
    wget https://download.bbbike.org/osm/bbbike/NewYork/NewYork.osm.pbf && \
    wget https://download.bbbike.org/osm/bbbike/London/London.osm.pbf

COPY ./pittsburgh.osm /pittsburgh.osm
COPY ./initdb-postgis.sh /load_osm_data.sh
#RUN chmod 755 /load_data_osm.sh
