import cv2
import qualifications
import subprocess
from sys import platform as _platform
    
class Infiltrator:
    quali = qualifications.Qualifications()
	
    def process(self, path, compare=False):

        img = self.__load_image(path)
        bars, cut_imgs = self.__find_bars(img)
        for i in range(0, len(bars)):
            self.__draw_bar(img, bars[i])
            self.__OCR_image(cut_imgs[i])
        
        self.__show_image(img, 'canny')
        cv2.moveWindow('canny', 50, 50)
        
        if compare:
            img2 = self.__load_image(path)
            bars2, cut_imgs2 = self.__find_bars(img2, ['laplasjan'])
            
            for bar in bars2:
                self.__draw_bar(img2, bar)
				
            self.__show_image(img2, 'laplasjan')
            cv2.moveWindow('laplasjan', 900, 50)
        
        cv2.waitKey(0)

    def __load_image(self, path):
        print "Opening " + path
        img = cv2.imread(path)
        if img is None:
            raise Exception("There is no image under: " + path)
        return img

    def __filter_image(self, img, filters):

        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        if 'laplasjan' in filters:
            filtered = cv2.Laplacian(imgray, cv2.IPL_DEPTH_32F, ksize = 3)
		
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

            # Find 6-8 letters in bar TODO
            num_of_letters = len(self.quali.find_letters(cut_img))
            #print "Letters: " + str(num_of_letters)
            if not 4 <= num_of_letters < 9:
                continue
            
            # Find black on white ;)
            if not self.quali.is_histogram_valid(cut_img):
                 continue
            
            bars.append(contour)
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

    def __OCR_image(self, img):
        if _platform == "win32":
            params = list()
            params.append(cv2.cv.CV_IMWRITE_PNG_COMPRESSION)
            params.append(8)
            cv2.imwrite("OCR_candidate.png", img, params)
            
            args = ("OCR/tesseract.exe", 'OCR_candidate.png', "out")
                    
            #Or just:
            #args = "bin/bar -c somefile.xml -d text.txt -r aString -f anotherString".split()
            popen = subprocess.Popen(args, stdout=subprocess.PIPE)
            popen.wait()
            output = popen.stdout.read()
            
            f = open('out.txt')
            finalString = f.readline()
            f.close()
            print "Read plate:", finalString
        elif _platform == "linux" or _platform == "linux2":
            print "TODO"
            
