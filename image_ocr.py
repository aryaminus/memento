import os
import sys

import PIL.Image as Im
import pyocr
import pyocr.builders
from PIL import Image as Im
from pyocr import tesseract as tool


class iocr(object):
    
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

    def main(self, text_img_name):
        
        txt = tool.image_to_string(
            Im.open(text_img_name), lang=self.lang,
            builder=pyocr.builders.TextBuilder()
        )

        return txt
                
def image_ocr_main(text_img_name):
    #print(path)
    s = iocr()
    txt = s.main(text_img_name) # Def main to path
    return txt
