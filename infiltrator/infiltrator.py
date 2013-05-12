import cv2


class Infiltrator:
    def process(self, path):

        img = self.__load_image(path)
        bar = self.__find_bars(img)
        #self.__draw_bar(img, bar)
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
            area = w * h
            """ Real rectangle size """

            #print area
            #Pokaze wyciety fragment. Uwaga, bo moze byc duzo tych fragmentow i bedzie spam okienek...
            #cut_img = img[y:y + h, x:x + w]
            #cv2.imshow('image', cut_img)
            #cv2.waitKey(0)

            # At reasonable size
            if area < 500:
                continue

            # Find rectangles of reasonable ratio
            if w / h < 2.0 or w / h > 5.0:
                continue

            # Find 6-8 letters in bar TODO

            # Find black on white ;) TODO paste here Jacob ;>

            # Draw for debug
            self.__draw_bar(img, contour)
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