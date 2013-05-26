import cv2
import os
import re
import qualifications


class Infiltrator:
    quali = qualifications.Qualifications()
    __img = None

    def process(self, path, compare=False, show=False):

        img = self.__load_image(path)
        self.__img = self.__load_image(path)
        bars, cut_imgs = self.__find_bars(img, ['laplasjan']) # TODO cany was default
        possible_numbers = {}
        return_number = None

        for bar in bars:
            self.__draw_bar(img, bar)
            #docelowo malujemy jeden, wybrany
            self.__draw_bar(self.__img, bar)

        if show:
            self.__show_image(img, 'canny')
            cv2.moveWindow('canny', 50, 50)

        if compare:
            img2 = self.__load_image(path)
            bars2, cut_imgs2 = self.__find_bars(img2, ['laplasjan'])

            for bar in bars2:
                self.__draw_bar(img2, bar)

            if show:
                self.__show_image(img2, 'laplasjan')
                cv2.moveWindow('laplasjan', 900, 50)

        possible_numbers = self.__get_possible_numbers(cut_imgs, show)
        print possible_numbers

        if len(possible_numbers) == 1:
            return_number = possible_numbers.keys()[0]

        if show:
            cv2.waitKey(0)

        return return_number

    def __load_image(self, path, verbose=False):
        root_path = os.path.dirname(os.path.dirname(__file__))
        full_path = os.path.join(root_path, path)
        print "Opening " + full_path
        if verbose:
            print "Opening " + full_path
        img = cv2.imread(full_path)
        if img is None:
            raise Exception("There is no image under: " + full_path)            
        return img

    def __filter_image(self, img, filters):

        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if 'laplasjan' in filters:
            filtered = cv2.Laplacian(imgray, cv2.IPL_DEPTH_32F, ksize=3)

        if 'canny' in filters:
            filtered = cv2.Canny(imgray, 100, 100)

        return filtered

    def __find_bars(self, img, filters=['canny']):

        bars = []
        cut_imgs = []
        filtered = self.__filter_image(img, filters)

        contours, hierarchy = cv2.findContours(filtered, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

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

            # Find black on white ;)
            if not self.quali.is_histogram_valid(cut_img):
                continue

            num_of_letters = len(self.quali.find_letters(cut_img, show=False, fake=True))
            #print "Letters: " + str(num_of_letters)
            if not 4 <= num_of_letters < 9:
                continue

            bars.append(contour)
            #cut_imgs.append(self.__filter_image(cut_img, 'laplasjan'))

            cut_imgs.append(cut_img)
        return bars, cut_imgs

    def __draw_bar(self, img, bar):
        bound_rect = cv2.boundingRect(bar)
        pt1 = (bound_rect[0], bound_rect[1])
        pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
        cv2.rectangle(img, pt1, pt2, (0, 255, 0), 2)

    def __show_image(self, img, window):
        #Pomniejszenie obrazka
        img = cv2.resize(img, (800, 600))
        cv2.imshow(window, img)

    def show_image(self):
        self.__show_image(self.__img, 'image')
        cv2.waitKey(0)

    def __get_possible_numbers(self, cut_imgs, show):
        possible_numbers = {}
        for bar_img in cut_imgs:            
            word = self.quali.find_letters(bar_img, show)            
            word = self.__remove_special_chars(word)
            if __debug__:
                print "Validating: %s" % word
            if self.__can_be_plate(word):
                if word in possible_numbers:
                    possible_numbers[word] += 1
                else:
                    possible_numbers[word] = 1
        return possible_numbers

    def __can_be_plate(self, word):
        #return True
        pattern = re.compile("^([a-z]{2}\w{5}|[a-z]{3}\w{4})$", re.IGNORECASE)
        result = pattern.search(word)
        if not result:
            return None
        else:
            return result.group(0)

    def __remove_special_chars(self, word):
        return ''.join(e for e in word if e.isalnum())

