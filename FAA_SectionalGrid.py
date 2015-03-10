'''
Created on Aug 14, 2013

@author: kyleg
'''
import arcpy
#create Quads and Quarter Quad Grids that match the FAA Sectionals
arcpy.GridIndexFeatures_cartography("F:/Cart/projects/Graticule/MKC15.shp","#","NO_INTERSECTFEATURE","NO_USEPAGEUNIT","#","0.25 DecimalDegrees","0.25 DecimalDegrees","-97 36","16","28","1","NO_LABELFROMORIGIN")
arcpy.GridIndexFeatures_cartography("F:/Cart/projects/Graticule/ICT15.shp","#","NO_INTERSECTFEATURE","NO_USEPAGEUNIT","#","0.25 DecimalDegrees","0.25 DecimalDegrees","-104 36","16","28","1","NO_LABELFROMORIGIN")
arcpy.GridIndexFeatures_cartography("F:/Cart/projects/Graticule/ICT75.shp","#","NO_INTERSECTFEATURE","NO_USEPAGEUNIT","#","0.125 DecimalDegrees","0.125 DecimalDegrees","-104 36","32","56","1","NO_LABELFROMORIGIN")
arcpy.GridIndexFeatures_cartography("F:/Cart/projects/Graticule/MKC75.shp","#","NO_INTERSECTFEATURE","NO_USEPAGEUNIT","#","0.125 DecimalDegrees","0.125 DecimalDegrees","-97 36","32","56","1","NO_LABELFROMORIGIN")