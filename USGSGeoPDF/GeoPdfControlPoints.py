'''
Created on Aug 1, 2013

@author: kyleg
'''
import glob
from decimal import Decimal
list_of_files = glob.glob('C:\Gtiffinfo1\*.txt')# create the list of file
for file_name in list_of_files:
  FI = open(file_name, 'r')
  print FI
  FO = open(file_name.replace('CA_', 'CP_'), 'w')
  buffer = []
  blnk = ' '
  newline = '\n'
  for line in FI:
    if line.startswith("Up"): #Read Control Point info
    x = line[15:25]
    y = line[26:38]
    lond = line[41:44]
    lonm = line[45:47]
    lons = line[48:53]
    latd = line[57:59]
    latm = line[60:62]
    lats = line[63:68]
    londd = Decimal(lond.strip(' "')) # Convert to decimal
    lonmd = Decimal(lonm.strip(' "'))
    lonsd = Decimal(lons.strip(' "'))
    londecdeg = (londd + lonmd/60 + lonsd/3600)* -1 #Convert to decimal degrees
    londdstr = "%11.6f" % londecdeg
    latdd = Decimal(latd.strip(' "'))
    latmd = Decimal(latm.strip(' "'))
    latsd = Decimal(lats.strip(' "'))
    latdecdeg = latdd + latmd/60 + latsd/3600
    latddstr = "%9.6f" % latdecdeg
    buffer.append(x)
    buffer.append(blnk)
    buffer.append(y)
    buffer.append(blnk)
    buffer.append(londdstr)
    buffer.append(blnk)
    buffer.append(latddstr)
    buffer.append(newline)
    FO.write("".join(buffer))
  #now reset our state
    buffer = []
- See more at: http://ideas.arcgis.com/ideaView?id=087300000008DUZAA2#sthash.UdylySdP.dpuf