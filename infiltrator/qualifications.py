import cv2
import numpy as np
import os 
from pytesser import *

class Qualifications:
    def find_letters(self, img):
        letters = []
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        height, width = len(img), len(img[0])
        canny = cv2.Canny(imgray, 100, 200)
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            """ Real rectangle size """
            img = img[y:y + h, x:x + w]
            area = w * h

            # At reasonable size related to whole
            if not 0.45 < float(h) / height < 0.95:
                continue

            if not 0.04 < float(w) / width < 0.2:
                continue

            overlep = False
            for letter in letters:
                x2, y2, w2, h2 = cv2.boundingRect(letter)
                if self.is_intersection(x, y, x + w, y + h,
                                        x2, y2, x2 + w2, y2 + h2):
                    overlep = True
                    break

            if overlep:
                continue
            
            if h < 60:
                continue
            #self.draw_bar(imgray, contour)
            
            letters.append(contour)

        # For debug
        if len(letters) > 0:
        
            #sortuj po x
            letters.sort(key=lambda letter: letter[0,0,0])
                        
            i=0;
            word = ''
            for l in letters:
                x, y, w, h = cv2.boundingRect(l)
                letter = imgray[y:y+h,x:x+w]
                cv2.imwrite(str(i)+'.tif', letter)
                word = word + image_file_to_string(str(i)+'.tif').rstrip()
                i+=1
            
            print word
            cv2.imshow('image', imgray)
            cv2.waitKey(0)

        return letters

    def calc_histogram(self, img):

        if len(img.shape) != 2:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        h = np.zeros((300, 256, 3))
        cv2.equalizeHist(img)
        hist_item = cv2.calcHist([img], [0], None, [16], [0, 255])
        cv2.normalize(hist_item, hist_item, 0, 255, cv2.NORM_MINMAX)
        hist = np.int32(np.around(hist_item))

        for x, y in enumerate(hist):
            for i in range(0, 15):
                cv2.line(h, (x * 16 + i, 0), (x * 16 + i, y), (255, 255, 255))

        y = np.flipud(h)
        return y, hist

    def is_histogram_valid(self, cut_img):
        histogram_img, histogram = self.calc_histogram(cut_img)
        histogram = list(histogram)

        max_val = max(histogram)
        count = 0

        for element in histogram:
            if element >= 0.5 * max_val:
                count += 1

        #Za duzo wysokich slupkow oznacza cos dzikiego :P TODO
        if count > 6:
            #cv2.imshow('histogram', histogram_img)
            #cv2.imshow('image', cut_img)
            #cv2.waitKey(0)
            print 'rejecting'
            return False
        return True

    def is_intersection(self, ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):

        if (self.is_point_in_rectangle(ax1, ay1, bx1, by1, bx2, by2)
            or self.is_point_in_rectangle(ax1, ay2, bx1, by1, bx2, by2)
            or self.is_point_in_rectangle(ax2, ay1, bx1, by1, bx2, by2)
            or self.is_point_in_rectangle(ax2, ay2, bx1, by1, bx2, by2)
            or self.is_point_in_rectangle(bx1, by1, ax1, ay1, ax2, ay2)
            or self.is_point_in_rectangle(bx2, by1, ax1, ay1, ax2, ay2)
            or self.is_point_in_rectangle(bx1, by2, ax1, ay1, ax2, ay2)
            or self.is_point_in_rectangle(bx2, by2, ax1, ay1, ax2, ay2)):
            return True
        return False


    def is_point_in_rectangle(self, x, y, rx1, ry1, rx2, ry2):
        return rx1 <= x <= rx2 and ry1 <= y <= ry2

