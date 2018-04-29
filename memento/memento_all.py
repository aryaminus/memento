import os
import sys
from subprocess import call

from image_make import image_make_main
from .tess_ocr.ocr_orientation import ocr_orientation_main
from .tess_ocr.ocr_rename import ocr_rename_main
from .tess_ocr.ocr_save import ocr_save_main

VALIDITY = [".jpg",".gif",".png",".tga",".tif",".bmp"]

class ArgumentMissingException(Exception):
    def __init__(self):
        print("usage: {} <dirname>".format(sys.argv[0]))
        sys.exit(1)
    
def check_path(path):
    	return bool(os.path.exists(path)) #Checkif path exists

def main(path):
    call(['clear'])
    j = 1
    i = 0
    if call(['which', 'tesseract']): #Run the command described by args
        print("tesseract-ocr missing") #No tesseract installed
    while(True):
        sys.stdout.write("\t\t\t Memento: Meme Organizer \t \n\n")
        sys.stdout.write("Files in Directory: \t \n\n")

        if check_path(path):
            arr = os.listdir(path)
            for f in arr:
                ext = os.path.splitext(f)[1]
                if ext.lower() in VALIDITY:
                    print('[' + str(j) + ']' + ' ' + f ) 
                    j +=1
                                 
        else :
            print("No directory : " + format(path))

        print('\nChoose one or all: ')
        file = input()
        if file == 'all':
            prompt = " [1/2/3/4/5]: "
            sys.stdout.write("\n")
            sys.stdout.write(' 1) Orientation Check \n 2) Rename file \n 3) Save OCR \n 4) Edit text \n 5) Exit \n (Can you multiple inputs)' + prompt)
            choice = input()
            while (i != len(choice)):
                print ('\n\t\t\t Current Choice: ' + choice[i] + '\n')
                if choice[i] == '1':
                    ocr_orientation_main(path)
                    print(" Orientation Check DONE!! \n")
                elif choice[i] == '2':
                    ocr_rename_main(path)
                    print("Rename to identified text DONE!! \n")
                elif choice[i] == '3':
                    ocr_save_main(path)
                    print("Save the OCR to /OCR-text/ DONE!! \n")
                elif choice[i] == '4':
                    image_make_main(path)
                    print("Edit the text in image DONE!! \n")
                elif choice[i] == '5':
                    print("\t\t\t Thank you for using Memento!")
                    sys.exit(1)
                elif choice[i] == ' ':
                    print("Chosing Next! \n")
                else:
                    sys.stdout.write("Invalid Choice \n")
            i += 1

if __name__ == '__main__': #Execute all code before reading source file, ie. execute import, evaluate def to equal name to main
    if len(sys.argv) != 2: # Count number of arguments which contains the command-line arguments passed to the script if it is not equal to 2 ie for (py main.py 1_arg 2_arg)
        raise ArgumentMissingException
    path = sys.argv[1] #python main.py "path_to/img_dir" ie the argv[1] value
    path = os.path.abspath(path) #Accesing filesystem for Return a normalized absolutized version of the pathname path
    main(path)
    #s = memento(path)
    #s.main(path) # Def main to path