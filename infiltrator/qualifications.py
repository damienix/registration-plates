import cv2
import numpy as np
import os
from pytesser import *


class Qualifications:
    def find_letters(self, img, fake=False, show=True):
        """
        @type fake: bool
        fake -- returning fake letters speeds it up (default False)
        """
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

            if self.__is_overlapping_existing_letter(letters, h, w, x, y):
                continue

            if h < 60:
                continue
                self.draw_bar(imgray, contour)

            letters.append(contour)
        
        word = ''
        if len(letters) > 0:
            #sortuj po x
            letters.sort(key=lambda letter: letter[0, 0, 0])

            i = 0
            for l in letters:
                if not fake:
                    x, y, w, h = cv2.boundingRect(l)
                    letter = imgray[y:y + h, x:x + w]
                    cv2.imwrite('tmp/%d.tif' % i, letter)
                    word = word + image_file_to_string('tmp/%d.tif' % i).rstrip()
                    i += 1
                else:
                    word += 'X'

            angle = self.__get_plate_angle(imgray)
            imgray = self.__rotate(imgray, angle)
            if show:
                cv2.imshow('image', imgray)
                cv2.waitKey(0)
                
            
            

        return word
        
    def __get_plate_angle(self, img2):
        img = np.copy(img2)
        rows,cols = img.shape[:2]
        
        
        ret, tresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
        cv2.bitwise_not(tresh,img)
        element = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3));
        eroded = cv2.erode(img, element);
        
        points = []
        for i in range(0, rows):
            for j in range(0, cols):
                if eroded[i,j]==0:
                    points.append((i,j))

        box = cv2.minAreaRect(np.array(points));
        angle = box[2]
        if (angle < -45):
            angle += 90
            
        print 'Plate angle: ' + str(angle)
        
        return angle
        
    def __rotate(self, img, angle):
    
        rows,cols = img.shape[:2]
        image_center = tuple(np.array(img.shape)/2)
        rot_mat = cv2.getRotationMatrix2D((image_center[0], image_center[1]), -angle, 1)
        result = cv2.warpAffine(img, rot_mat,(cols,rows))

        #img = np.copy(result)
        #cv2.imshow('image', img)
        #cv2.waitKey(0)
        return result

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

    def __is_overlapping_existing_letter(self, letters, h, w, x, y):
        overlap = False
        for letter in letters:
            x2, y2, w2, h2 = cv2.boundingRect(letter)
            if self.__is_intersection(x, y, x + w, y + h,
                                      x2, y2, x2 + w2, y2 + h2):
                overlap = True
                break
        return overlap

    def __is_intersection(self, ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):

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

