'''
Created on Aug 8, 2013

@author: kyleg
'''
import arcpy, os
arcpy.env.overwriteOutput = True
sr = arcpy.GetParameterAsText(0)
sr = arcpy.SpatialReference(3419)
#3419 = NAD_1983_StatePlane_Kansas_North_FIPS_1501_Feet
#3420 = NAD_1983_StatePlane_Kansas_South_FIPS_1502_Feet
print sr.name

CAF = arcpy.GetParameterAsText(1)
CAF = '0.99992146'
print CAF

DGN_IN = arcpy.GetParameterAsText(2)
DGN_IN = r'C:\pwworking\kyleg\dms90199\slt_ROW_exist.dgn'

drive, path = os.path.splitdrive(DGN_IN)
path, filename = os.path.split(path)
fileName, fileExtension = os.path.splitext(filename)

print drive
print path
print filename
print fileName

wsout = arcpy.GetParameterAsText(3)
wsout = r'C:\pwworking\kyleg\dms90199'

newcs = str(sr)+fileName

csr = arcpy.SpatialReference(newcs)

PAF = 1/float(CAF)
print str(PAF) + " is the PAF"

print csr.name
print csr.GCSName

DGN_IN = r'C:\pwworking\kyleg\dms90199\slt_ROW_exist.dgn'

print csr.name
print "original easting = "+str(sr.falseEasting)
csr.falseEasting.fset = sr.falseEasting*PAF
print "modified easting = "+str(csr.falseNorthing)
print "original Northing = "+str(sr.falseNorthing)
csr.falseNorthing = sr.falseNorthing*PAF
print "modified Northing = "+str(csr.falseNorthing)
print "original scale factor = "+str(sr.scaleFactor)
csr.scaleFactor = PAF
print "modified scale factor = "+str(csr.scaleFactor)

spatial_ref = arcpy.Describe(DGN_IN).spatialReference

if spatial_ref.name == "Unknown Coordinate System":
        print("{0} has an unknown spatial reference".format(DGN_IN))
        
else:
        print("{0} : {1}".format(DGN_IN, spatial_ref.name))

arcpy.DefineProjection_management(DGN_IN,csr)

print "DGN reference defined"

if arcpy.Exists(drive+path+"\\"+fileName+".gdb"):
    arcpy.Delete_management(drive+path+"\\"+fileName+".gdb")
    arcpy.CreateFileGDB_management(drive+path, fileName) 
    pass
else:
    arcpy.CreateFileGDB_management(drive+path, fileName) 

DGN_IN_ALL = (DGN_IN+"\\Polyline", DGN_IN+"\\Annotation", DGN_IN+"\\Point",DGN_IN+"\\Polygon", DGN_IN+"\\MultiPatch")

arcpy.FeatureClassToGeodatabase_conversion(DGN_IN_ALL, drive+path+"\\"+fileName+".gdb")








