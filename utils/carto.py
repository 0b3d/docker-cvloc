import os 

def removeTextXML(mapfile, new_mapfile_name):
# This function removes all text labels and shields in the stylesheet.
    text = 'TextSymbolizer'
    shields = 'ShieldSymbolizer'
    #text = 'Parameter'
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
    mapfile = os.path.join( os.environ['carto'], 'style_s2v.xml')
    removeTextXML(mapfile, new_mapfile_name='style_s2v_notxt_bheight_newyork.xml')
    #addLines(mapfile)