'''
Created on Apr 25, 2016

@author: kyleg
'''

xmldir = r'\\prodnet\acceptTRS'
#acutal server is dt00ne55

def Main():
    PrintXMLDocList()

def PrintXMLDocList():
    from stat import S_ISREG, ST_CTIME, ST_MODE
    import os
    import time
    
    dirpath = xmldir
    
    entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
    entries = ((os.stat(path), path) for path in entries)
    entries = ((stat[ST_CTIME], path) for stat, path in entries if S_ISREG(stat[ST_MODE]))
               
    for cdate, path in sorted(entries):
        print time.ctime(cdate), os.path.basename(path)

if __name__ == '__main__':
    pass