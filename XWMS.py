'''
Created on Jul 31, 2013

@author: kyleg

create an XWMS file that sets the WMS extents for Each County via the bounding box

example XWMS file:
'''
l1 ='<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n'
l2 ='<BentleyWMSFile>\n'
l3 = '    <VERSION>1.3</VERSION>\n'
l4 ='    <URL>http://kdot3:YN8WP6MA@www.valtus.ca/views/wms</URL>\n'
l5='    <REQUEST>\n'
l6='        <VERSION>1.1.1</VERSION>\n'
l7='        <SRS>EPSG:3857</SRS>\n'
l8='        <LAYERS>0</LAYERS>\n'
l9='        <STYLES />\n'
l10='        <FORMAT>image/jpeg</FORMAT>\n'
l11='        <TRANSPARENT>FALSE</TRANSPARENT>\n'
l13='    </REQUEST>\n'
l14='    <MAPEXTENT>\n'
l15xxx='        <BBOX>-11361548.9799927,4430394.07407966,-10526646.0085542,4875031.97002587</BBOX>\n'
l16='    </MAPEXTENT>\n'
l17='    <LayerList>\n'
l18='        <LAYER TITLE="VCP" NAME="VCP"  ABSTRACT="An optimized layer that is a world mosaic of the best imagery in the Valtus archive. This Layer has been specifically designed to be used as a base imagery layer for both web and desktop applications." />\n'
l19='    </LayerList>\n'
l20='    <SERVICE>\n'
l21='        <MAXWIDTH>1024</MAXWIDTH>\n'
l22='        <MAXHEIGHT>1024</MAXHEIGHT>\n'
l23='    </SERVICE>\n'
l24='    <EditorData>\n'
l25='        <RangeMethod>Manual</RangeMethod>\n'
l26='        <LayerRange>Intersection</LayerRange>\n'
l27='        <UseModelCoordSysUsefulRange>False</UseModelCoordSysUsefulRange>\n'
l28='        <UseMapCoordSysUsefulRange>True</UseMapCoordSysUsefulRange>\n'
l29='        <ExplicitSRS>True</ExplicitSRS>\n'
l30='    </EditorData>\n'
l31='</BentleyWMSFile>'
firstpart = l1+l2+l3+l4+l5+l6+l7+l8+l9+l10+l11+l13+l14
secondpart =l16+l17+l18+l19+l20+l21+l22+l23+l24+l25+l26+l27+l28+l29+l30+l31

#!shape.extent.XMax!  -used to calculate min&max X&Y on county layer in ArcMap

import arcpy
ws = r'\\gisdata\arcgis\GISdata\KDOT\DESIGN\XWMS\valtus'
fc = r'\\gisdata\arcgis\GISdata\KDOT\DESIGN\COUNTY_XWMS_GEN.gdb\COUNTY_WMERC'
field = "COUNTY_NAME"
minx="MinX"
miny="MinY"
maxx="MaxX"
maxy="MaxY"
cursor = arcpy.SearchCursor(fc)
for row in cursor:
    cname = str(row.getValue(field))+'.xwms'
    iminx = str(row.getValue(minx))
    imaxx = str(row.getValue(maxx))
    iminy = str(row.getValue(miny))
    imaxy = str(row.getValue(maxy))
    print cname
    l15 ='        <BBOX>'+str(iminx)+','+str(iminy)+','+str(imaxx)+','+str(imaxy)+'</BBOX>\n'
    print l15
    statement = firstpart + l15+secondpart
    output = open(cname, 'w')
    output.write(statement)

