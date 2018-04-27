import io
import os
import subprocess
import sys
import time
from subprocess import call

import PIL.Image as Im
import pyocr
import pyocr.builders
from PIL import Image as Im
from wand.image import Image

VALIDITY = [".jpg",".gif",".png",".tga",".tif",".bmp", ".pdf"]

FNULL = open(os.devnull, 'w') #Open file in write mode to The file path of the null device. For example: '/dev/null' 

class ArgumentMissingException(Exception):
    def __init__(self):
        print("usage: {} <dirname>".format(sys.argv[0]))
        sys.exit(1)

class saram(object):
    
    def __init__(self):
        
        ocr_language = 'eng'

        #if call(['which', 'tesseract']): #Run the command described by args
        #    print("tesseract-ocr missing") #No tesseract installed
        
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            print("No OCR tool found")
            sys.exit(1)
        self.tool = tools[0]
        print("OCR tool: %s" % self.tool)

        try:
            langs = self.tool.get_available_languages()
            self.lang = langs[0]
            if ocr_language in langs:
                self.lang = ocr_language
            print("OCR selected language: %s (available: %s)" % (self.lang.upper(), ", ".join(langs)))
        except Exception as e:
            print("{}".format(e))
    
    def create_directory(self, path):
        if not os.path.exists(path): #No path
	        os.makedirs(path) #Create path
    
    def pdf_run(self, image_file_name, filename):
        
        image_pdf = Image(filename=image_file_name, resolution=300) #take filename
        image_page = image_pdf.convert("png") #png conversion

        page = 1 #init page
        process_start = time.time()

        for img in image_page.sequence: # Every single image in image_page for grayscale conversion in 300 resolution
            
            img_per_page = Image(image=img)
            img_per_page.type = 'grayscale'
            img_per_page.depth = 8
            img_per_page.density = 300

            try:
                img_per_page.level(black=0.3, white=1.0, gamma=1.5, channel=None)
            
            except AttributeError as e:
                print("Update Wand library: %s" % e)

            img_buf = path + '/' + "saram_" + filename + str(page) + ".png"
            img_per_page.save(filename=img_buf)

            page_start = time.time()

            page_elaboration = time.time() - page_start

            print("page %s - size %s - process %2d sec." % (page, img_per_page.size, page_elaboration))
                
            page += 1
            img.destroy()

        process_end = time.time() - process_start
        print("Total elaboration time: %s" % process_end)
    
    def get_rotation_info(self, filename):
        arguments = ' %s - -psm 0'
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
        if bool(os.path.exists(path)):
            directory_path = path + '/OCR-text/' #Create text_conversion folder
            count = 0
            other_files = 0

            for f in os.listdir(path):
                ext = os.path.splitext(f)[1] #Split the pathname path into a pair i.e take .png/ .jpg etc

                if ext.lower() == ".pdf": #For PDF
                    image_file_name = path + '/' + f #Full /dir/path/filename.extension
                    filename = os.path.splitext(f)[0] #Filename without extension
                    filename = ''.join(e for e in filename if e.isalnum() or e == '-') #Join string of filename if it contains alphanumeric characters or -
                    self.pdf_run(image_file_name, filename)

            for f in os.listdir(path):
                ext = os.path.splitext(f)[1] #Split the pathname path into a pair i.e take .png/ .jpg etc

                if ext.lower() == ".pdf": #For PDF
                    continue

                if ext.lower() in VALIDITY:
                    image_file_name = path + '/' + f #Full /dir/path/filename.extension
                    
                    degrees = self.get_rotation_info(image_file_name)
                    print(degrees)
                    if degrees:
                        self.fix_dpi_and_rotation(image_file_name, degrees, ext)

            for f in os.listdir(path): #Return list of files in path directory

                ext = os.path.splitext(f)[1] #Split the pathname path into a pair i.e take .png/ .jpg etc
                
                image_file_name = path + '/' + f #Full /dir/path/filename.extension
                filename = os.path.splitext(f)[0] #Filename without extension
                filename = ''.join(e for e in filename if e.isalnum() or e == '-') #Join string of filename if it contains alphanumeric characters or -
                text_file_path = directory_path + filename #Join dir_path with file_name

                if ext.lower() not in VALIDITY: #Convert to lowercase and check in validity list          
                    other_files += 1 #Increment if other than validity extension found
                    continue

                if count == 0: #No directory created
                    self.create_directory(directory_path) #function to create directory
                count += 1

                if ext.lower() == ".pdf": #For PDF
                    continue

                else:
                    """
                    degrees = self.get_rotation_info(image_file_name)

                    if degrees:
                        self.fix_dpi_and_rotation(image_file_name, degrees, ext)
                    """
                    
                    call(["tesseract", image_file_name, text_file_path], stdout=FNULL) #Fetch tesseract with FNULL in write mode

                print(str(count) + (" file" if count == 1 else " files") + " processed")
            
            for f in os.listdir(path):
                 if f.startswith("saram_"):
                    os.remove(os.path.join(path, f))

            if count + other_files == 0:
                print("No files found") #No files found
            else :
                print(str(count) + " / " + str(count + other_files) + " files converted")
        else :
            print("No directory : " + format(path))

if __name__ == '__main__': #Execute all code before reading source file, ie. execute import, evaluate def to equal name to main
    if len(sys.argv) != 2: # Count number of arguments which contains the command-line arguments passed to the script if it is not equal to 2 ie for (py main.py 1_arg 2_arg)
        raise ArgumentMissingException
    path = sys.argv[1] #python main.py "path_to/img_dir" ie the argv[1] value
    path = os.path.abspath(path) #Accesing filesystem for Return a normalized absolutized version of the pathname path
    s = saram()
    s.main(path) # Def main to path
