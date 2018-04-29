import numpy
import PIL.Image as Im
from PIL import Image as Im

import cv2


# Selects the image coords for the Twitter pic
def getContourCoords(pic_contour):
	y0 = min(pic_contour[0][0][1],pic_contour[1][0][1],pic_contour[2][0][1],pic_contour[3][0][1])
	y1 = max(pic_contour[0][0][1],pic_contour[1][0][1],pic_contour[2][0][1],pic_contour[3][0][1])
	x0 = min(pic_contour[0][0][0],pic_contour[1][0][0],pic_contour[2][0][0],pic_contour[3][0][0])
	x1 = max(pic_contour[0][0][0],pic_contour[1][0][0],pic_contour[2][0][0],pic_contour[3][0][0])
	return (y0,y1,x0,x1)

class croper(object):
    
    def __init__(self):
        print('Cropping in process')

    # Add a white border to every image
    def addWhiteBorder(self, filename):
        im_naked = Im.open(filename)
        naked_size = im_naked.size
        bordered_size = (int(naked_size[0]*1.1), int(naked_size[1]*1.1))
        im_bordered = Im.new("RGB", bordered_size, color = (255,255,255))
        im_bordered.paste(im_naked, ((bordered_size[0]-naked_size[0])//2,(bordered_size[1]-naked_size[1])//2))
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
        pic_img_name = 'Mem_' + filename + ext
        pic_img_name = directory_path_pic + pic_img_name
        cv2.imwrite(pic_img_name,im_cropped)

    def main(self, image_file_name, filename, directory_path_text, directory_path_pic, ext):
                
        border = self.addWhiteBorder(image_file_name)
        im = self.convertPILtoOpenCV(border)
        contour = self.getContours(im)
        pic_contour = self.getPicContour(contour)
        self.saveCroppedImages(im, pic_contour, filename, directory_path_text, directory_path_pic, ext)

def image_crop_main(image_file_name, filename, directory_path_text, directory_path_pic, ext):
    #print(path)
    s = croper()
    s.main(image_file_name, filename, directory_path_text, directory_path_pic, ext) # Def main to path
