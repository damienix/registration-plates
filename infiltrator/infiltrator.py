import cv2
import numpy as np


class Infiltrator:
    def process(self, path):

        img = self.__load_image(path)
        bars = self.__find_bars(img)

        for bar in bars:
            self.__draw_bar(img, bar)

        self.__show_image(img)
        cv2.waitKey(0)

    def __load_image(self, path):
        print "Opening " + path
        img = cv2.imread(path)
        if img is None:
            raise Exception("There is no image under: " + path)
        return img

    def __find_bars(self, img):

        bars = []
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(imgray, 100, 100)
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            """ Real rectangle size """
            cut_img = img[y:y + h, x:x + w]
            area = w * h

            # At reasonable size
			# this might be misleading - e.g. are we guaranteed to have a photo of a whole car, and not 800x600 plate only?
            if area < 500:			
                continue

            # Find rectangles of reasonable ratio
            if not 2.0 < w / h < 5.0:
                continue

            # Find 6-8 letters in bar TODO
            if not 5 < len(self.__find_letters(cut_img)) < 9:
                continue

            # Find black on white ;)
            # if not self.__is_histogram_valid(cut_img):
            #     continue

            bars.append(contour)

        return bars


    def __draw_bar(self, img, bar):
        bound_rect = cv2.boundingRect(bar)
        pt1 = (bound_rect[0], bound_rect[1])
        pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
        cv2.rectangle(img, pt1, pt2, (255, 255, 0), 2)

    def __show_image(self, img):
        #Pomniejszenie obrazka
        img = cv2.resize(img, (800, 600))
        cv2.imshow('image', img)

    def __find_letters(self, cut_img):
        return [1, 1, 1, 2, 1, 1]  # TODO fake objects for now

    def __calc_histogram(self, img):
        h = np.zeros((300, 256, 3))
        if len(img.shape) != 2:
            im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        hist_item = cv2.calcHist([img], [0], None, [16], [0, 255])

        cv2.normalize(hist_item, hist_item, 0, 255, cv2.NORM_MINMAX)
        hist = np.int32(np.around(hist_item))

        for x, y in enumerate(hist):
            for i in range(0, 15):
                cv2.line(h, (x * 16 + i, 0), (x * 16 + i, y), (255, 255, 255))

        y = np.flipud(h)
        return y, hist

    def __is_histogram_valid(self, cut_img):
        histogram_img, histogram = self.__calc_histogram(cut_img)
        #uncomment those 3 for debug
        # cv2.imshow('histogram', histogram_img)
        # cv2.imshow('image', cut_img)
        # cv2.waitKey(0)
