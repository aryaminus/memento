import os
import subprocess

import PIL.Image as Im
from PIL import Image as Im

VALIDITY = [".jpg",".gif",".png",".tga",".tif",".bmp"]

class orientation(object):
    
    def __init__(self):
        print('Orientation check in process')
    
    def get_rotation_info(self, filename):
        arguments = ' %s - -psm 0'
        filename = "'" + filename + "'" #Needed as filename need to be in quotes having spaces which is not accepted direct in  subprocess
        # /to/dir = '/to/dir'
        stdoutdata = subprocess.getoutput('tesseract' + arguments % filename)
        degrees = None

        for line in stdoutdata.splitlines():
            print(line)
            info = 'Orientation in degrees: '
            if info in line:
                degrees = -float(line.replace(info, '').strip())
        return degrees

    def fix_dpi_and_rotation(self, filename, degrees, ext):
        im1 = Im.open(filename)
        print('Fixing rotation %.2f in %s...' % (degrees, filename))
        im1.rotate(degrees).save(filename)
        
    def main(self, path):

        count = 0
        other_files = 0

        for f in os.listdir(path): #Return list of files in path directory

            ext = os.path.splitext(f)[1] #Split the pathname path into a pair i.e take .png/ .jpg etc

            if ext.lower() not in VALIDITY: #Convert to lowercase and check in validity list          
                other_files += 1 #Increment if other than validity extension found
                continue

            else:

                count += 1
                c=0
                while c!=2:
                    image_file_name = path + '/' + f #Full /dir/path/filename.extension
                    degrees = self.get_rotation_info(image_file_name)
                    print(degrees)
                    if degrees:
                        self.fix_dpi_and_rotation(image_file_name, degrees, ext)
                    c += 1

                print(str(count) + (" file" if count == 1 else " files") + " processed")

        if count + other_files == 0:
            print("No files found") #No files found
        else :
            print(str(count) + " / " + str(count + other_files) + " files converted")

def ocr_orientation_main(path):
    print(path)
    s = orientation()
    s.main(path) # Def main to path
