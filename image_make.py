import os
import sys
from image_crop import image_crop_main
from image_ocr import image_ocr_main

VALIDITY = [".jpg",".gif",".png",".tga",".tif",".bmp"]

class maker(object):
    
    def __init__(self):
        print('Cropping in process')
    
    def create_directory(self, directory_path_text,directory_path_pic):
        if not os.path.exists(directory_path_text): #No path
	        os.makedirs(directory_path_text) #Create path
        if not os.path.exists(directory_path_pic): #No path
	        os.makedirs(directory_path_pic) #Create path]
  
    def editext(self, text):
        while True:
            print('Current text:' + text + '\n')
            prompt = " [1/2/3/4]: "
            sys.stdout.write(' \n 1) Edit text \n 2) Replace word \n 3) Change complete \n ' + prompt)
            choice = input().lower().strip()
            if choice[0] == '1':
                print ('Enter new text:')
                text = input()
            elif choice[0] == '2':
                print('Enter word to replace:')
                orig = input()
                print('\n Enter the new word:')
                new = input()
                text.replace(orig, new)
            elif choice[0] == '3':
                break
            else:
                sys.stdout.write("Invalid Choice \n")
        return text

    def main(self, path):
        directory_path_text = path + '/image/' #Create text_conversion folder
        directory_path_pic = path + '/pic/' #Create text_conversion folder
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

                #image_

                print(str(count) + (" file" if count == 1 else " files") + " processed")

        if count + other_files == 0:
            print("No files found") #No files found
        else :
            print(str(count) + " / " + str(count + other_files) + " files converted")

def image_make_main(path):
    print(path)
    s = maker()
    s.main(path) # Def main to path
