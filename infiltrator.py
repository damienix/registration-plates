import cv2


class Infiltrator:
    def process(self, path):
        print path
        img = cv2.imread(path)

        if img is None:
            raise Exception("There is no image under: " + path)

        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(imgray, 100, 100);

        contours, hierarchy = cv2.findContours(canny, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        max_area = 0

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:
                x, y, w, h = cv2.boundingRect(contour)
                cut_img = img[y:y + h, x:x + w]

                #print area
                #Pokaze wyciety fragment. Uwaga, bo moze byc duzo tych fragmentow i bedzie spam okienek...
                #cv2.imshow('image', cut_img)
                #cv2.waitKey(0)

                if (area > max_area):
                    max_area = area
                    bar = contour

        bound_rect = cv2.boundingRect(bar)
        pt1 = (bound_rect[0], bound_rect[1])
        pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])

        cv2.rectangle(img, pt1, pt2, (255, 255, 0), 2)

        #Pomniejszenie obrazka
        img = cv2.resize(img, (800, 600))

        cv2.imshow('image', img)
        cv2.waitKey(0)
