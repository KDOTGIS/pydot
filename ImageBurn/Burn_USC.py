'''
Created on Mar 22, 2016

@author: kyleg
'''

import Image
import glob, os


infile = r'C:\temp\photodir'
burnimage = infile+'\USC2.png'

size = 480, 640

for infile in glob.glob("*.jpg"):
    file, ext = os.path.splitext(infile)
    im = Image.open(infile)
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(file + ".thumbnail", "JPEG")


'''
for root, subdirs, files in os.walk(DIRECTORY):
    for image in files:
        if os.path.splitext(image)[1].lower() in ('.jpg', '.jpeg'):
            jpgimage = os.path.join(root, image)
            photoname = os.path.splitext(image)[0]
            oldtype = '.jpg'
            newtype = '.png'
            photo = os.path.join(photoname+oldtype)
            pngname = os.path.join(photoname+newtype)
            print jpgimage, pngname, photo
            photo = Image.open(photo)
            photo.save(photoname, "PNG")
            #photo.convert('RGBA').save(jpgimage, 'PNG')
            '''
  

            #foreground = Image.open(burnimage)
            #background.paste(foreground, (0, 0), foreground)
            
            