'''
Created on Aug 8, 2013

@author: kyleg
'''
import os, shutil, arcpy
appdata = os.getenv('APPDATA')
wsuser = appdata+"\ESRI\Desktop10.1\ArcMap\Coordinate Systems"

print "appdata"
sr = arcpy.GetParameterAsText(0)
sr = arcpy.SpatialReference(3419)

srxs = arcpy.SpatialReference(sr)
sr = srxs.loadFromString(srxs)

CAF = arcpy.GetParameterAsText(1)
#CAF = '0.99992146'

PRJ_Out = arcpy.GetParameterAsText(2)

prjfile = wsuser+"\\"+PRJ_Out+'.prj'
print prjfile

#print str(sr.name) + " is the proj name"
#print str(sr.falseOriginAndUnits) + " is the false origin, units"
#print str(sr.falseEasting)  + " is the false easting"
adjEast = float(sr.falseEasting) * 1/float(CAF)
print str(adjEast)  + " is the adjusted false easting"
adjNorth = float(sr.falseNorthing) * 1/float(CAF)
print str(adjNorth) + " is the adjusted false northing"
print str(sr.scaleFactor) + " is the scale factor"
adjScaleFac = 1/float(CAF)

srstr = sr.exportToString()
print srstr 
adjsr1 = srstr.replace('"Scale_Factor",1.000000', '"Scale_Factor",'+ str(adjScaleFac))
adjsr2 = adjsr1.replace("1312333.333333333", str(adjEast))
print adjsr2

dstfile = wsuser+"\\KDOT"+PRJ_Out+".prj"
shutil.copy2(prjfile, dstfile)

'''
srnew = arcpy.SpatialReference()
srnew.loadFromString()
srnew.create()

dstfile = wsuser+"\\KDOT"+PRJ_Out+".prj"
shutil.copy2(prjfile, dstfile)

tempFile = open(dstfile, 'w' )
tempFile.write(adjsr2)
tempFile.close()


tempFile = open(dstfile, 'w' )

ScaleToSearch = '1.000000'
ScaleToReplace = str(PAF)

for line in fileinput.input(dstfile,0):
    tempFile.write(line.replace(ScaleToSearch, ScaleToReplace))
    tempFile.close()
'''