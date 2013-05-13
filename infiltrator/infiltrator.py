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
            num_of_letters = len(self.__find_letters(cut_img))
            #print "Letters: " + str(num_of_letters)
            if not 4 <= num_of_letters < 9:
                continue
            
            # Find black on white ;)
            if not self.__is_histogram_valid(cut_img):
                 continue

            bars.append(contour)

        return bars


    def __draw_bar(self, img, bar):
        bound_rect = cv2.boundingRect(bar)
        pt1 = (bound_rect[0], bound_rect[1])
        pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
        cv2.rectangle(img, pt1, pt2, (0, 255, 0), 2)

    def __show_image(self, img):
        #Pomniejszenie obrazka
        img = cv2.resize(img, (800, 600))
        cv2.imshow('image', img)

    def __find_letters(self, img):
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
                if self.__is_intersection(x, y, x + w, y + h,
                                          x2, y2, x2 + w2, y2 + h2):
                    overlep = True
                    break

            if overlep:
                continue

            self.__draw_bar(imgray, contour)
            letters.append(contour)

        # For debug
        # if len(letters) > 0:
        #     cv2.imshow('image', imgray)
        #     cv2.waitKey(0)

        return letters

    def __calc_histogram(self, img):
		
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

    def __is_histogram_valid(self, cut_img):
		histogram_img, histogram = self.__calc_histogram(cut_img)
		histogram = list(histogram)
		
		max_val = max(histogram)
		count = 0
		
		for element in histogram:
			if element>=0.5*max_val:
				count+=1
		
		#Za duzo wysokich slupkow oznacza cos dzikiego :P
		if count > 6:
			#cv2.imshow('histogram', histogram_img)
			#cv2.imshow('image', cut_img)
			#cv2.waitKey(0)
			print 'rejecting'
			return False
        
		return True

    def __is_intersection(self, ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):

        if (self.__is_point_in_rectangle(ax1, ay1, bx1, by1, bx2, by2)
            or self.__is_point_in_rectangle(ax1, ay2, bx1, by1, bx2, by2)
            or self.__is_point_in_rectangle(ax2, ay1, bx1, by1, bx2, by2)
            or self.__is_point_in_rectangle(ax2, ay2, bx1, by1, bx2, by2)
            or self.__is_point_in_rectangle(bx1, by1, ax1, ay1, ax2, ay2)
            or self.__is_point_in_rectangle(bx2, by1, ax1, ay1, ax2, ay2)
            or self.__is_point_in_rectangle(bx1, by2, ax1, ay1, ax2, ay2)
            or self.__is_point_in_rectangle(bx2, by2, ax1, ay1, ax2, ay2)):
            return True
        return False


    def __is_point_in_rectangle(self, x, y, rx1, ry1, rx2, ry2):
        return rx1 <= x <= rx2 and ry1 <= y <= ry2

