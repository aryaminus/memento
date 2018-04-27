# OCR to convert pdf image to text and save it as csv file
# Note the dependencies

import re
import csv
import urllib2
from cStringIO import StringIO
try:
	from pdfminer.pdfinterp import PDFResourceManager, process_pdf
except:
	from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

from wand.image import Image
from PIL import Image as PI
import pyocr
from pyocr import tesseract as tool
import pyocr.builders
import io


def pdf_from_url_to_txt(filename):
		# Create a PDF resource manager object that stores shared resources.
		infp = file(filename, 'rb')
		rsrcmgr = PDFResourceManager()
		outfp = StringIO()
		# becuase pdf documents are utf-8
    	#codec = 'utf-8'
		laparams=LAParams()
		
		# Create a csv device object.
		device = TextConverter(rsrcmgr, outfp, codec='utf-8', laparams=laparams)
		try:
			process_pdf(rsrcmgr, device, infp)
		except:
			PDFPageInterpreter(rsrcmgr, device)
		strOut = outfp.getvalue()
		
		return strOut
    
#list of all the pdf links, links can be local pathname as well
localLinks = [link]
outputOCR = csv.writer(open('outputOCR.csv', 'w'), delimiter='`',quotechar='"',lineterminator='\n')
outputOCR.writerow(['Index', 'Text'])

# URL link for the file
for index, link in enumerate(localLinks):
	#try:
	output=pdf_from_url_to_txt(str(link))
	others = str(output)
	print ('_________________________')
	print (index+1, ':', link)
	
	if len(others) ==0:
		#tool = pyocr.get_available_tools()
		#lang = tool.get_available_languages()[1]

		req_image = []
		final_text = []

		image_pdf = Image(filename=link, resolution=300)
		image_jpeg = image_pdf.convert('jpeg')

		for img in image_jpeg.sequence:
			img_page = Image(image=img)
			req_image.append(img_page.make_blob('jpeg'))

		for img in req_image: 
			txt = tool.image_to_string(
				PI.open(io.BytesIO(img)),
				builder=pyocr.builders.TextBuilder()
			)
			final_text.append(txt)

		others = str(final_text)
		print ('Others:', others)
		
	else:
		print ('Others:', others)
	
	outputOCR.writerow([index, others])
	
print ('********************End********************')
