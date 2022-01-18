""" This script can be used to generate map tiles from OSM data.   
    Configure options in the bottom of the file.
    Use 18 for S1 and 19 for S2
 """

import os
import multiprocessing
import pandas as pd
import mapnik

def render_and_save(m, output, metadata, zoom=18, size=224):
   
    # Define size of tile
    if type(size) == tuple:
        width = size[0]
        height = size[1]
    else: 
        width, height = size, size

    # target projection
    projection = '+proj=aeqd +ellps=WGS84 +lat_0={} +lon_0={}'.format(90, -metadata['yaw'] + metadata['lon'])
    merc = mapnik.Projection(projection)
    # WGS lat/long source projection of centrel 
    longlat = mapnik.Projection('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
    
    # ensure the target map projection is mercator
    m.srs = merc.params()
    
    # transform the centre point into the target coord sys
    centre = mapnik.Coord(metadata['lon'], metadata['lat'])  
    transform = mapnik.ProjTransform(longlat, merc)
    merc_centre = transform.forward(centre)
    print(merc_centre)

    
    # 360/(2**zoom) degrees = 256 px
    # so in merc 1px = (20037508.34*2) / (256 * 2**zoom)
    # hence to find the bounds of our rectangle in projected coordinates + and - half the image width worth of projected coord units
    dx = ((20037508.34*2*(width/2)))/(width*(2 ** (zoom)))
    minx = merc_centre.x - dx
    maxx = merc_centre.x + dx
    
    # grow the height bbox, as we only accurately set the width bbox
    m.aspect_fix_mode = mapnik.aspect_fix_mode.ADJUST_BBOX_HEIGHT

    bounds = mapnik.Box2d(minx, merc_centre.y-10, maxx, merc_centre.y+10) # the y bounds will be fixed by mapnik due to ADJUST_BBOX_HEIGHT
    m.zoom_to_box(bounds)

    # render the map image to a file
    mapnik.render_to_file(m, output)

class RenderThread:
    def __init__(self, save_dir, q, printLock):
        self.save_dir = save_dir
        self.q = q 
        self.printLock = printLock

    def render_tile(self, i, row, tile_url, zoom):
        render_and_save(m, tile_url,zoom=zoom, metadata=row, size=(width, height))
        print('tile {}/{} output to {}'.format(i, n, tile_url))

    def loop(self):
        while True:
            # Fetch a tile from the queue and render it
            r = self.q.get()
            if (r == None):
                self.q.task_done()
                break
            else:
                (i, row, zoom, tile_url) = r

            exists = ''
            if os.path.isfile(tile_url):
                exists = "exists"
            else:
                self.render_tile(i, row, tile_url, zoom)

            bytes=os.stat(tile_url)[6]
            empty= ''
            if bytes == 103:
                empty = " Empty Tile "
            if bytes == 857:
                empty = " Gray tile "
            if exists != '':
                print(exists)
            if empty != '':
                print(empty)


            self.printLock.acquire()
            self.printLock.release()
            self.q.task_done()

def render_locations(locations, num_threads, save_dir):
    queue = multiprocessing.JoinableQueue(32)
    printLock = multiprocessing.Lock()
    renderers = {}
    for i in range(num_threads):
        renderer = RenderThread(save_dir, queue, printLock)
        render_thread = multiprocessing.Process(target=renderer.loop)
        render_thread.start()
        renderers[i] = render_thread

    for i in range(len(locations)):
        row = locations.iloc[i, :]
        for zoom in zoom_levels:
            tile_url = os.path.join(save_dir, 'z' + str(zoom), row['pano_id'] + '.png')
            t = (i, row, zoom, tile_url)
            queue.put(t)
 
    for i in range(num_threads):
        queue.put(None)

    queue.join()

    for i in range(num_threads):
        renderers[i].join()


##### ------ Define dataset to render and output directory --------
city = 'bristol'                                # This is the name of the postgres database name, in our case pittsburgh and newyork
save_dir = "temp/bristoltest"
csv_filename = 'temp/test.txt'                  # File with locations to be rendered, expects 4 columns id, yaw, lat, lon (no header row)
num_threads = 4
width = 256
height = 256
zoom_levels = [18]          # Use 18 for S1 and 19 for S2
mapfile = os.path.join(os.environ['carto'],'style_notxt_bristol.xml')

# --- 

frame = pd.read_csv(csv_filename, names=["pano_id","yaw","lat","lon"])
n = len(frame)
print("Nodes to process in {} dataset: {}".format( csv_filename, n))

# Create directories
for zoom in zoom_levels:
    directory = os.path.join(save_dir,'z' + str(zoom))
    if not os.path.isdir(directory):
        print("Creating directory", directory)
        os.makedirs(directory)

# Load mapfile
m = mapnik.Map(width, height) 
mapnik.load_map(m, mapfile)

render_locations(frame, num_threads, save_dir)

