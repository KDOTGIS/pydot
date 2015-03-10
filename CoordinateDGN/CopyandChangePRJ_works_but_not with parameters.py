'''
Created on Aug 8, 2013

@author: kyleg
'''
import os, shutil, fileinput, arcpy
appdata = os.getenv('APPDATA')
wsuser = appdata+r"\ESRI\Desktop10.1\ArcMap\Coordinate Systems"
#PRJ_in = arcpy.GetParameterAsText(0)
#srcfile = wsuser+"\\CUSTOM_NAD_1983_StatePlane_Kansas_North_FIPS_1501_Feet.prj"
cs = str(arcpy.SpatialReference(PRJ_in).name)
srcfile = wsuser+"\\"+cs

PRJ_in = arcpy.SpatialReference("NAD_1983_StatePlane_Kansas_North_FIPS_1501_Feet.prj")
print PRJ_in.name


CAF = arcpy.GetParameterAsText(1)
#CAF = '0.99992146'
PRJ_Out = arcpy.GetParameterAsText(2)
#dstfile = wsuser+"\\CUSTOM_K839204.prj"
dstfile = wsuser+"\\KDOT"+PRJ_Out+".prj"

PAF = 1/float(CAF)

shutil.copy2(srcfile, dstfile)

fileName, fileExtension = os.path.splitext(dstfile)

oldFileName  = fileName+"_old"+fileExtension
tempFileName = fileName+"_temp"+fileExtension

tempFile = open(tempFileName, 'w' )

ScaleToSearch = '1.000000'
ScaleToReplace = str(PAF)

for line in fileinput.input(dstfile):
    tempFile.write(line.replace(ScaleToSearch, ScaleToReplace))
    tempFile.close()
    
os.rename(dstfile, oldFileName)
os.rename(tempFileName, dstfile)

oldFileName  = fileName+"_old"+fileExtension
tempFileName = fileName+"_temp"+fileExtension

tempFile = open(tempFileName, 'w' )

OffsetToSearch = '1312333.333333333'
OffsetToReplace = str(float (OffsetToSearch)*(PAF))
for line in fileinput.input(dstfile):
    tempFile.write( line.replace(OffsetToSearch, OffsetToReplace) )
    tempFile.close()
    
os.remove(dstfile)
oldFileName  = fileName+"_old"+fileExtension
os.remove(fileName+"_old"+fileExtension)
shutil.copy2(fileName+"_temp"+fileExtension, dstfile)
os.remove(fileName+"_temp"+fileExtension)
'''