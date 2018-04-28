import sys
import os
from subprocess import call

from ocr_rename import ocr_rename_main
from ocr_orientation import ocr_orientation_main
#from ocr_save import ocr_save_main

class ArgumentMissingException(Exception):
    def __init__(self):
        print("usage: {} <dirname>".format(sys.argv[0]))
        sys.exit(1)
    
def check_path(path):
    	return bool(os.path.exists(path)) #Checkif path exists

def main(path):
    if call(['which', 'tesseract']): #Run the command described by args
    	print("tesseract-ocr missing") #No tesseract installed
    elif check_path(path):
        prompt = " [1/2/3]: "
        sys.stdout.write(' 1) Orientation Check \n 2) Rename \n 3) Save OCR ' + prompt)
        choice = input().lower().strip()
        if choice[0] == '1':
            ocr_orientation_main(path)
        if choice[0] == '2':
            ocr_rename_main(path)
        if choice[0] == '3':
            #ocr_save_main(path)
            print('Yo')
        else:
            sys.stdout.write("Invalid Choice \n")
        
    else :
        print("No directory : " + format(path))

if __name__ == '__main__': #Execute all code before reading source file, ie. execute import, evaluate def to equal name to main
    if len(sys.argv) != 2: # Count number of arguments which contains the command-line arguments passed to the script if it is not equal to 2 ie for (py main.py 1_arg 2_arg)
        raise ArgumentMissingException
    path = sys.argv[1] #python main.py "path_to/img_dir" ie the argv[1] value
    path = os.path.abspath(path) #Accesing filesystem for Return a normalized absolutized version of the pathname path
    main(path)
    #s = memento(path)
    #s.main(path) # Def main to path