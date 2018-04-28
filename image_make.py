import os
import subprocess
import time

import numpy
import PIL.Image as Im
from PIL import Image as Im

import cv2

VALIDITY = [".jpg",".gif",".png",".tga",".tif",".bmp"]

# Selects the image coords for the Twitter pic
def getContourCoords(pic_contour):
	y0 = min(pic_contour[0][0][1],pic_contour[1][0][1],pic_contour[2][0][1],pic_contour[3][0][1])
	y1 = max(pic_contour[0][0][1],pic_contour[1][0][1],pic_contour[2][0][1],pic_contour[3][0][1])
	x0 = min(pic_contour[0][0][0],pic_contour[1][0][0],pic_contour[2][0][0],pic_contour[3][0][0])
	x1 = max(pic_contour[0][0][0],pic_contour[1][0][0],pic_contour[2][0][0],pic_contour[3][0][0])
	return (y0,y1,x0,x1)

class maker(object):
    
    def __init__(self):
        print('Cropping in process')
    
    def create_directory(self, directory_path_text,directory_path_pic):
        if not os.path.exists(directory_path_text): #No path
	        os.makedirs(directory_path_text) #Create path
        if not os.path.exists(directory_path_pic): #No path
	        os.makedirs(directory_path_pic) #Create path

    # Add a white border to every image
    def addWhiteBorder(self, filename):
        im_naked = Im.open(filename)
        naked_size = im_naked.size
        bordered_size = (int(naked_size[0]*1.1), int(naked_size[1]*1.1))
        im_bordered = Im.new("RGB", bordered_size, color = (255,255,255))
        im_bordered.paste(im_naked, ((bordered_size[0]-naked_size[0])/2,(bordered_size[1]-naked_size[1])/2))
        return im_bordered

    # Converts PIL image format to OpenCV format
    def convertPILtoOpenCV(self, border):
        open_cv_image = numpy.array(border)[:, :, ::-1].copy()
        return open_cv_image

    # Use OpenCV to find the contours of the input image
    def getContours(self, im):
        im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im_gray = cv2.bilateralFilter(im_gray, 11, 17, 17)
        ret, thresh = cv2.threshold(im_gray, 240, 240, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    # Select the second largest rectangular contour
    def getPicContour(self, contours):
        # sort the contours by area, of these, take the top ten largest contours
        contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
        pic_contour = None
        count = 0
        for contour in contours:
            # approximate the shape of the contour
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            if len(approx) == 4:
                pic_contour = approx
                count = count + 1
                if count == 2:
                    break
        return pic_contour

    def fix_dpi_and_rotation(self, filename, degrees, ext):
        im1 = Im.open(filename)
        print('Fixing rotation %.2f in %s...' % (degrees, filename))
        im1.rotate(degrees).save(filename)

    # Crop the input image around the pic coords, and save the cropped image
    # also crops the input image around the text, and saves the cropped text
    def saveCroppedImages(self, im, pic_contour, filename, directory_path_text, directory_path_pic, ext):
        (y0,y1,x0,x1) = getContourCoords(pic_contour)
        text_cropped = im[0:y0,:]
        text_img_name = filename + '_text' + ext
        text_img_name = directory_path_text + text_img_name
        cv2.imwrite(text_img_name,text_cropped)
        # print "Text component saved as: " + str(text_img_name)
        im_cropped = im[y0:y1, x0:x1]
        pic_img_name = filename + '_pic' + ext
        pic_img_name = directory_path_pic + pic_img_name
        cv2.imwrite(pic_img_name,im_cropped)

    def main(self, path):
        directory_path_text = path + '/image/' #Create text_conversion folder
        directory_path_pic = path + '/image/' #Create text_conversion folder
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
                
                border = self.addWhiteBorder(image_file_name)
                im = self.convertPILtoOpenCV(border)
                contour = self.getContours(im)
                pic_contour = self.getPicContour(contour)
                self.saveCroppedImages(im, pic_contour, filename, directory_path_text, directory_path_pic, ext)

                print(str(count) + (" file" if count == 1 else " files") + " processed")

        if count + other_files == 0:
            print("No files found") #No files found
        else :
            print(str(count) + " / " + str(count + other_files) + " files converted")

def image_make_main(path):
    print(path)
    s = maker()
    s.main(path) # Def main to path
