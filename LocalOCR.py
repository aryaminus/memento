#!/usr/bin/python
# coding: utf-8

import argparse
import io
import os
import re
import sys
import time

import pyocr
import pyocr.builders
from PIL import Image as PI
from wand.image import Image

import tesserocr
from tesserocr import PSM, RIL, PyTessBaseAPI


class LocalOCR(object):
	
    def __init__(self, ocr_language):
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

    def process(self, pdf_filename, pdf_resolution, imageformat, do_orientation):
        final_text = ""
        image_pdf = Image(filename=pdf_filename, resolution=pdf_resolution)
        image_page = image_pdf.convert(imageformat)

        page = 1
        process_start = time.time()
        for img in image_page.sequence:
            img_per_page = Image(image=img)
            img_per_page.type = 'grayscale'
            img_per_page.depth = 8
            img_per_page.density = 300
            try:
                img_per_page.level(black=0.3, white=1.0, gamma=1.5, channel=None)
            except AttributeError as e:
                print("Update Wand library: %s" % e)
            img_per_page.save(filename="buffer.png")
            page_start = time.time()
            txt = self.image2txt_pyocr(img_per_page.make_blob(imageformat), do_orientation)
            page_elaboration = time.time() - page_start
            print("page %s - size %s - process %2d sec. - text %s" %
                  (page, img_per_page.size, page_elaboration, len(txt)))
            final_text += "%s\n" % txt
            page += 1
            img.destroy()

        process_end = time.time() - process_start
        print("Total elaboration time: %s" % process_end)

        return final_text

    def image2txt_pyocr(self, image, do_orientation):
        txt = ""
        orientation = ""
        img_per_page = PI.open(io.BytesIO(image))

        if do_orientation is True:
            try:
                if self.tool.can_detect_orientation():
                    orientation = self.tool.detect_orientation(img_per_page, lang=self.lang)
                    angle = orientation["angle"]
                    if angle != 0:
                        img_per_page.rotate(orientation["angle"])
            except pyocr.PyocrException as exc:
                print("Orientation detection failed: {}".format(exc))
            print("Orientation: {}".format(orientation))

        try:
            txt = self.tool.image_to_string(
                img_per_page, lang=self.lang,
                builder=pyocr.builders.TextBuilder()
            )
        except pyocr.error.TesseractError as e:
            print("{}".format(e))
        return txt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process input PDF file to CSV by OCR')
    parser.add_argument('pdf_filename', nargs='?', default='INPUT.pdf',
                        help='Input PDF file')
    parser.add_argument('pdf_resolution', nargs='?', default=300,
                        help='Input PDF dpi resolution')
    parser.add_argument('ocr_language', nargs='?', default='eng',
                        help='OCR language')
    parser.add_argument('ocr_imageformat', nargs='?', default='png',
                        help='OCR image format')
    parser.add_argument('ocr_do_orientation', nargs='?', default=True,
                        help='OCR do orientation test')
    parser.add_argument('text_output', nargs='?', default="output.txt",
                        help='OCR text output')
    args = parser.parse_args()

    if not args.pdf_filename:
        print('--filename is mandatory')
        sys.exit(1)

    p = LocalOCR(args.ocr_language)

    print("1. TEXT file \"%s\" not found - Process PDF file \"%s\"" % (args.text_output, args.pdf_filename))
    output = p.process(args.pdf_filename, args.pdf_resolution, args.ocr_imageformat, args.ocr_do_orientation)
    print("2 Writing TEXT output file \"%s\"" % args.text_output)
    file = open(args.text_output, "wb")
    for i in output:
        file.write(i.encode("utf-8"))
    file.close()
