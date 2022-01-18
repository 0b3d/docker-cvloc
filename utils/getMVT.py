import psycopg2 
import re
import json 
from pyproj import Proj, transform

DATABASE = {
   'user':     'postgres',
   'host':     'localhost',
   'port':     '5432',
   'database': 'newyork'
   }


# Table to query for MVT data, and columns to
# include in the tiles.
TABLE = {
    'table':       'planet_osm_polygon',
    'srid':        '3857',
    'geomColumn':  'way',
    'attrColumns': 'osm_id, amenity, building'
    }  


class MVTProvider():
    #def __init__(self):
    DATABASE_CONNECTION = None

    # Calculate envelope in "Spherical Mercator" (https://epsg.io/3857)
    def tileToEnvelope(self, tile):
        # Width of world in EPSG:3857
        worldMercMax = 20037508.3427892
        worldMercMin = -1 * worldMercMax
        worldMercSize = worldMercMax - worldMercMin
        # Width in tiles
        worldTileSize = 2 ** tile['zoom']
        # Tile width in EPSG:3857
        tileMercSize = worldMercSize / worldTileSize
        # Calculate geographic bounds from tile coordinates
        # XYZ tile coordinates are in "image space" so origin is
        # top-left, not bottom right
        env = dict()
        env['xmin'] = worldMercMin + tileMercSize * tile['x']
        env['xmax'] = worldMercMin + tileMercSize * (tile['x'] + 1)
        env['ymin'] = worldMercMax - tileMercSize * (tile['y'] + 1)
        env['ymax'] = worldMercMax - tileMercSize * (tile['y'])
        return env

    # Generate SQL to materialize a query envelope in EPSG:3857.
    # Densify the edges a little so the envelope can be
    # safely converted to other coordinate systems.
    def envelopeToBoundsSQL(self, env):
        DENSIFY_FACTOR = 4
        env['segSize'] = (env['xmax'] - env['xmin'])/DENSIFY_FACTOR
        sql_tmpl = 'ST_Segmentize(ST_MakeEnvelope({xmin}, {ymin}, {xmax}, {ymax}, 3857),{segSize})'
        return sql_tmpl.format(**env)    

    # Generate a SQL query to pull a tile worth of MVT data
    # from the table of interest.        
    def envelopeToSQL(self, env):
        tbl = TABLE.copy()
        tbl['env'] = self.envelopeToBoundsSQL(env)
        # Materialize the bounds
        # Select the relevant geometry and clip to MVT bounds
        # Convert to MVT format
        sql_tmpl = """
            WITH 
            bounds AS (
                SELECT {env} AS geom, 
                       {env}::box2d AS b2d
            ),
            mvtgeom AS (
                SELECT ST_AsMVTGeom(ST_Transform(t.{geomColumn}, 3857), bounds.b2d) AS geom, 
                       {attrColumns}
                FROM {table} t, bounds
                WHERE ST_Intersects(t.{geomColumn}, ST_Transform(bounds.geom, {srid}))
            ) 
            SELECT ST_AsMVT(mvtgeom.*) FROM mvtgeom
        """
        return sql_tmpl.format(**tbl)

    def query_buildings(self, env):
        tbl = {
            'table': 'planet_osm_polygon',
            'srid':  '3857',
            'geomColumn':  'way',
            'attrColumns': "osm_id, name, building, tags->'height' as height"
            }  
        tbl['env'] = self.envelopeToBoundsSQL(env)
        # Materialize the bounds
        # Select the relevant geometry and clip to MVT bounds
        # Convert to MVT format
        sql_tmpl = """
            WITH 
            bounds AS (
                SELECT {env} AS geom, 
                       {env}::box2d AS b2d
            ),
            mvtgeom AS (
                SELECT ST_AsMVTGeom(ST_Transform(t.{geomColumn}, 3857), bounds.b2d) AS geom, 
                       {attrColumns}
                FROM {table} t, bounds
                WHERE ST_Intersects(t.{geomColumn}, ST_Transform(bounds.geom, {srid})) and building is not null
            ) 
            SELECT ST_AsMVT(mvtgeom.*) FROM mvtgeom
        """
        return sql_tmpl.format(**tbl)

    # Run tile query SQL and return error on failure conditions
    def sqlToPbf(self, sql):
        # Make and hold connection to database
        if not self.DATABASE_CONNECTION:
            #try:
            self.DATABASE_CONNECTION = psycopg2.connect(**DATABASE)
            #except (Exception, psycopg2.Error) as error:
            #    self.send_error(500, "cannot connect: %s" % (str(DATABASE)))
            #    return None

        # Query for MVT
        with self.DATABASE_CONNECTION.cursor() as cur:
            cur.execute(sql)
            if not cur:
                #self.send_error(404, "sql query failed: %s" % (sql))
                return None
            return cur.fetchone()[0]
        
        return None


if __name__ == "__main__":
    mp = MVTProvider()
    #mp.tileToEnvelope(tile)
    dx = 100 # 30 meters
    
    lat, lon =  40.7237950,-74.0003670
    inProj = Proj(init='epsg:4326')
    outProj = Proj(init='epsg:3857')
    X, Y = transform(inProj,outProj,lon,lat)
    
    envelope = {'xmin': X-dx,
                'xmax': X+dx,
                'ymin': Y-dx,
                'ymax': Y+dx}
    #sql = mp.envelopeToSQL(envelope)
    sql = mp.query_buildings(envelope)
    pbf = mp.sqlToPbf(sql)
    print(pbf[1])
    #self.wfile.write(pbf)

    with open("test.mvt", "wb") as binary_file:
        # write text or bytes to the file 
        #binary_file.write("Write text by encoding\n".encode('utf8'))
        num_bytes_written = binary_file.write(pbf)
        print("Wrote %d bytes." % num_bytes_written)