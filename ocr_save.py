import os
import sys

import PIL.Image as Im
import pyocr
import pyocr.builders
from PIL import Image as Im
from pyocr import tesseract as tool

VALIDITY = [".jpg",".gif",".png",".tga",".tif",".bmp"]

class save(object):
    
    def __init__(self):
        
        ocr_language = 'eng'
        
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

    def savefile(self,initial, txt, directory_path):
        
        if (bool(os.path.exists(directory_path)) == False): #No directory created
            self.create_directory(directory_path) #function to create directory
        fw = open(directory_path + "/" + initial + ".txt" , "w+")
        fw.write(txt)
        fw.close()

        
    def main(self, path):

        directory_path = path + '/OCR-text/' #Create text_conversion folder
        count = 0
        other_files = 0

        for f in os.listdir(path): #Return list of files in path directory

            ext = os.path.splitext(f)[1] #Split the pathname path into a pair i.e take .png/ .jpg etc

            if ext.lower() not in VALIDITY: #Convert to lowercase and check in validity list          
                other_files += 1 #Increment if other than validity extension found
                continue

            else:

                count += 1
                image_file_name = path + '/' + f #Full /dir/path/filename.extension

                txt = tool.image_to_string(
                    Im.open(image_file_name), lang=self.lang,
                    builder=pyocr.builders.TextBuilder()
                )
                
                #txt = txt.split()[:5]
                initial = txt.replace('\a', ' ').replace('\b', ' ').replace('\f', ' ').replace('\n',' ').replace('\r', '').replace('\t',' ').replace('\v',' ') #.replace(' ','_') #.replace('.','_') #Replace \n and \t with space
                initial = initial[:60] #Take 1st 100 words
                print('Filename:' + initial + '\n')

                os.chmod(path, 0o777)
                self.savefile(initial, txt, directory_path)

                print(str(count) + (" file" if count == 1 else " files") + " processed")

        if count + other_files == 0:
            print("No files found") #No files found
        else :
            print(str(count) + " / " + str(count + other_files) + " files converted")

def ocr_save_main(path):
    print(path)
    s = save()
    s.main(path) # Def main to path
