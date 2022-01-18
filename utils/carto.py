import os 

def removeTextXML(mapfile, new_mapfile_name):
# This function removes all text labels and shields in the stylesheet.
    text = 'TextSymbolizer'
    shields = 'ShieldSymbolizer'
    # text = 'Parameter'
    newPath = os.path.join( os.environ['carto'], new_mapfile_name)
    newFile = open( newPath, "w")
    count = 0
    with open( mapfile , 'r') as f:
        for line in f:
            if text not in line and shields not in line and 'Font' not in line:
                newFile.write(line)
            else:
                count+=1
        newFile.close()
    print("Done, {} lines with {} text were removed".format(count, text))
    print("New file in ", newPath)


def removeAmenitiesXML(mapfile, new_mapfile_name):
# This function removes all text labels and shields in the stylesheet.
    #text = 'TextSymbolizer'
    #shields = 'ShieldSymbolizer'
    text = 'shop'
    # shields = 'amenity'
    # text = 'Parameter'
    newPath = os.path.join( os.environ['carto'], new_mapfile_name)
    newFile = open( newPath, "w")
    count = 0
    with open( mapfile , 'r') as f:
        for line in f:
            if 'Filter' in line:
                
                if 'amenity' in line and "[feature]" in line:
                    line = line.replace("amenity","none")
                    count+=1

                if 'bus_stop' in line and "[feature]" in line:
                    line = line.replace("bus_stop","none")
                    count+=1 

                if 'traffic_signals' in line and "[feature]" in line:
                    line = line.replace("traffic_signals","none")
                    count+=1 

                if 'shop' in line:
                    line = line.replace("'shop'","'none'")
                    count+=1
            
            newFile.write(line)

        newFile.close()
    print("Done, {} lines with {} text were replaced".format(count, text))
    print("New file in ", newPath)

def addLines(mapfile):
    mask = '<Parameter name="type"><![CDATA[postgis]]></Parameter>'
    lines = ['       <Parameter name="user"><![CDATA[postgres]]></Parameter>','       <Parameter name="host"><![CDATA[localhost]]></Parameter>']
    newPath = os.path.join( os.environ['carto'], "added_lines.xml")
    newFile = open( newPath, "w")
    count = 0
    
    with open( mapfile , 'r') as f:
        for line in f:
            newFile.write(line)
            if mask in line:
                for new_line in lines:
                    newFile.write(new_line + '\n')
                count+=1
        newFile.close()
    print("Done, {} instances added".format(count))
    print("New file in ", newPath)
       
    
if __name__ == "__main__":
    mapfile = os.path.join(os.environ['carto'], 'style_notxt_newyork.xml')
    #removeTextXML(mapfile, new_mapfile_name='style_no_amenities_newyork.xml')
    removeAmenitiesXML(mapfile, new_mapfile_name='style_no_amenities_newyork.xml')
    #addLines(mapfile)