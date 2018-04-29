import os
import shutil
import sys

from .image_crop import image_crop_main
from .image_join import image_join_main
from .image_ocr import image_ocr_main

VALIDITY = [".jpg",".gif",".png",".tga",".tif",".bmp"]

class maker(object):
    
    def __init__(self):
        print('Edit Initialization \n')
    
    def create_directory(self, directory_path_text,directory_path_pic):
        if not os.path.exists(directory_path_text): #No path
	        os.makedirs(directory_path_text) #Create path
        if not os.path.exists(directory_path_pic): #No path
	        os.makedirs(directory_path_pic) #Create path

    def editext(self, text):
        while True:
            print('\nCurrent text: \n' + text)
            prompt = " [1/2/3]: "
            sys.stdout.write(' \n 1) Edit text \n 2) Replace word \n 3) Change complete ' + prompt)
            choice = input()
            if choice[0] == '1':
                print ('\nEnter new text:')
                text = input()
            elif choice[0] == '2':
                print('\n Enter word to replace:')
                orig = input()
                print('\n Enter the new word:')
                new = input()
                text = text.replace(orig, new)
            elif choice[0] == '3':
                print('\nGot the new word!\n')
                break
            else:
                sys.stdout.write("Invalid Choice \n")
        return text

    def main(self, path):
        directory_path_text = path + '/text/' #Create text_conversion folder
        directory_path_pic = path + '/Memento/' #Create text_conversion folder
        count = 0
        other_files = 0

        for f in os.listdir(path): #Return list of files in path directory

            ext = os.path.splitext(f)[1] #Split the pathname path into a pair i.e take .png/ .jpg etc
            image_file_name = path + '/' + f #Full /dir/path/filename.extension
            filename = os.path.splitext(f)[0] #Filename without extension
            #filename = ''.join(e for e in filename if e.isalnum() or e == '-') #Join string of filename if it contains alphanumeric characters or -

            if ext.lower() not in VALIDITY: #Convert to lowercase and check in validity list          
                other_files += 1 #Increment if other than validity extension found
                continue

            else:
                if count == 0: #No directory created
                    self.create_directory(directory_path_text,directory_path_pic) #function to create directory

                count += 1

                image_crop_main(image_file_name, filename, directory_path_text, directory_path_pic, ext)
                
                text_img_name = filename + '_text' + ext
                text_img_name = directory_path_text + text_img_name                
                text = image_ocr_main(text_img_name)
                
                new_text = self.editext(text)

                pic_img_name = 'Mem_' + filename + ext
                pic_img_name = directory_path_pic + pic_img_name

                new_img_name = directory_path_pic + new_text + ext

                image_join_main(new_text, pic_img_name, path, new_img_name)

                print(str(count) + (" file" if count == 1 else " files") + " processed")

        if count + other_files == 0:
            print("No files found") #No files found
        else :
            print(str(count) + " / " + str(count + other_files) + " files converted")
            shutil.rmtree(path + '/text/')
            for f in os.listdir(directory_path_pic):
                if f.startswith("Mem_"):
                    os.remove(os.path.join(directory_path_pic, f))

def image_make_main(path):
    print(path)
    s = maker()
    s.main(path) # Def main to path
