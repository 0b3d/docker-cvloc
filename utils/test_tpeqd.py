import os
import mapnik 
from math import cos, sin, pi

width, height, zoom = 256,256,18
# Metadata canberra
# metadata = {
#     'yaw' : 180,
#     'lat' : -35.239846,
#     'lon' : 149.099469,
#     'easting' : 691033.725827,
#     'northing' : 6.098338e+06
# }

metadata = {
    'yaw' : 0,
    'lat' : 40.734852,
    'lon' : -73.990707,
}

# ------ Source projection -----------------------
# WGS latlong (epsg 4326)
source_proj = mapnik.Projection('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

# ------ Temporal merc projection  ----------------------
string = '+proj=merc +datum=WGS84 +k=1.0 +units=m +over +no_defs'
merc_proj = mapnik.Projection(string)

source_centre = mapnik.Coord(metadata['lon'], metadata['lat'])  
transform = mapnik.ProjTransform(source_proj, merc_proj)
merc_centre = transform.forward(source_centre)

tile_size_m = 40075016.68 / (2 ** zoom)    # This is the distance covered by a map tile in the equator given the zoom

#----- target projection ----------------------

# Two point equidistant projection: https://proj.org/operations/projections/tpeqd.html
# Also useful https://gist.github.com/eyeNsky/9853026
# https://desktop.arcgis.com/en/arcmap/latest/map/projections/two-point-equidistant.htm
# It is a generalization of the azimuthal equidistant projection.
# Neither conformal nor equal-area (Shapes, areas, distances, directions and angles are generally distorted)
# Distances from any of the two reference points are correct.
# Only supported with spheres

# Parameters are:
# False northing 
# False Northing
# Latitude of 1st point
# Latitude of 2nd point
# Longitude of 1st point
# Longitude of 2nd point


# Define points for the new projection
yaw = pi * metadata['yaw'] / 180

P1x = source_centre.x
P1y = source_centre.y

P2x = merc_centre.x + 10*tile_size_m*cos(-yaw) # Scale auxilary vector by 10
P2y = merc_centre.y + 10*tile_size_m*sin(-yaw) # Scale auxilary vector by 10
aux_point = mapnik.Coord(P2x, P2y)
aux_source = transform.backward(aux_point)
P2x = aux_source.x 
P2y = aux_source.y 


# create the string
string = '+proj=tpeqd +lat_1={} +lat_2={} +lon_1={} +lon_2={}  +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs'.format(P1y, P2y, P1x, P2x)
target_proj = mapnik.Projection(string)

# transform the centre point into the target coord sys
source_centre = mapnik.Coord(metadata['lon'], metadata['lat'])  
transform = mapnik.ProjTransform(source_proj, target_proj)
target_centre = transform.forward(source_centre)

dx = tile_size_m / 2 
minx = target_centre.x - dx
maxx = target_centre.x + dx

# Considering earth's circunference in equator to be 40075016.68 m
# The number of tiles in a slippy map depends on the zoom   n_tiles = 2**zoom
# Let's render the tiles with size 40075016.68 / (2 ** zoom)  (As in the equator)

# Create map
m = mapnik.Map(width, height) 
mapfile = os.path.join(os.environ['carto'],'style_notxt.xml')
mapnik.load_map(m, mapfile)
m.srs = target_proj.params()

# grow the height bbox, as we only accurately set the width bbox
m.aspect_fix_mode = mapnik.aspect_fix_mode.ADJUST_BBOX_HEIGHT
bounds = mapnik.Box2d(minx, target_centre.y-10, maxx, target_centre.y+10) # the y bounds will be fixed by mapnik due to ADJUST_BBOX_HEIGHT (y values don't matter here)

m.zoom_to_box(bounds)             # Set the geographic extent

# render the map image to a file
mapnik.render_to_file(m, 'test_tqed.png')

