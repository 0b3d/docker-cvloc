import psycopg2 
import re
import json 
import matplotlib.pyplot as plt
from pyproj import Proj, transform
from Location import Location
from shapely.geometry import LineString, MultiLineString, LinearRing
from shapely import wkb

#def lines2graph(lines):

DATABASE = {
   'user':     'postgres',
   'host':     'localhost',
   'port':     '5432',
   'database': 'newyork'
   }

class OSMDataProvider():
    def __init__(self, location, tile_size_in_meters=60):
        self.location = location
        self.size = tile_size_in_meters

        inProj = Proj(init='epsg:4326')
        outProj = Proj(init='epsg:3857')
        self.X, self.Y = transform(inProj,outProj,self.location.lon,self.location.lat)
        self.envelope = self.getEnvelope()
        #self.envelope = self.envelopeToBoundsSQL(self.envelope)
        
    DATABASE_CONNECTION = None

    def getEnvelope(self):
        # Calculate envelope in "Spherical Mercator" (https://epsg.io/3857)
        dx = self.size/2
    
        envelope = {'xmin': self.X-dx,
                'xmax': self.X+dx,
                'ymin': self.Y-dx,
                'ymax': self.Y+dx}
        return envelope

        # Show bbox
    def getEnvelopeBBOX(self):
        bbox = LinearRing([(self.envelope['xmin'],self.envelope['ymin']),
                        (self.envelope['xmin'],self.envelope['ymax']),
                        (self.envelope['xmax'],self.envelope['ymax']),
                        (self.envelope['xmax'],self.envelope['ymin'])])
        return bbox

    def execute_query(self, sql):
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
            return cur.fetchall()
        
        return None

    def envelopeToBoundsSQL(self, env):
        # Generate SQL to materialize a query envelope in EPSG:3857.
        # Densify the edges a little so the envelope can be
        # safely converted to other coordinate systems.
        DENSIFY_FACTOR = 4
        env['segSize'] = (env['xmax'] - env['xmin'])/DENSIFY_FACTOR
        sql_tmpl = 'ST_Segmentize(ST_MakeEnvelope({xmin}, {ymin}, {xmax}, {ymax}, 3857),{segSize})'
        return sql_tmpl.format(**env)    

    def query_buildings(self):
        tbl = {
            'table': 'planet_osm_polygon',
            'srid':  '3857',
            'geomColumn':  'way',
            'attrColumns': "osm_id, name, building, tags->'height' as height"
            }  
        tbl['env'] = self.envelopeToBoundsSQL(self.envelope)
        # Materialize the bounds
        # Select the relevant geometry and clip to MVT bounds
        # Convert to MVT format
        sql_tmpl = """
            WITH 
            bounds AS (
                SELECT {self.env} AS geom, 
                       {self.env}::box2d AS b2d
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

    def query_roads(self):
        tbl = {
            'table': 'planet_osm_line',
            'srid':  '3857',
            'geomColumn':  'way',
            'attrColumns': "highway"
            }  
        tbl['env'] = self.envelopeToBoundsSQL(self.envelope)
        # Materialize the bounds
        # Select the relevant geometry and clip to MVT bounds
        # Convert to MVT format
        sql_tmpl = """
            WITH 
            bounds AS (
                SELECT {env} AS geom, 
                       {env}::box2d AS b2d
            ),
            data AS (
                SELECT ST_Transform(t.{geomColumn}, 3857), bounds.b2d AS geom, 
                       {attrColumns}
                FROM {table} t, bounds
                WHERE ST_Intersects(t.{geomColumn}, ST_Transform(bounds.geom, {srid})) and highway is not null
            ) 
            SELECT * FROM data
        """
        query = sql_tmpl.format(**tbl)
        data = self.execute_query(query)
        
        lines = []
        types = []
        for line in data:
            geom = line[0]
            geom = wkb.loads(geom, hex=True) #Transform line to the format of shapely
            lines.append(geom)
            types.append(line[2])
        roads = MultiLineString(lines=lines)
        return (roads,types)


if __name__ == "__main__":
    loc = Location("hudsonriver5k", 989, 'manhattan', base_index='local')
    print(loc)
    provider = OSMDataProvider(loc, tile_size_in_meters=60)
    
    # Show center location
    plt.scatter(provider.X, provider.Y)

    # show
    bbox = provider.getEnvelopeBBOX()
    x,y = bbox.xy
    plt.plot(x,y)
    
    # Get lines
    roads, roads_types = provider.query_roads()
    print(roads, roads_types)

    for line in roads:
        #coords = list(line.coords)
        x,y = line.xy
        plt.plot(x,y)
        plt.scatter(x,y)
        intersection = bbox.intersection(line)
        print(intersection)
        #if intersection is no
        #for point in intersection:
        #    plt.scatter(point.x, point.y)

    plt.show()
    
