import cv2
import subprocess
from sys import platform as _platform
from PIL import Image

class Reader:
    def readText(self, cut_imgs):
        for img in cut_imgs:
            readStr = self.__OCR_image(img)
            readStr = readStr.replace(" ", "")
            print 'Read plate:', readStr
            
    def __OCR_image(self, img):
        
        # First write the image file
        params = list()
        params.append(cv2.cv.CV_IMWRITE_PNG_COMPRESSION)
        params.append(8)
        cv2.imwrite("OCR/OCR_candidate.png", img, params)
            
            
        #test -> clear image
        self.__boldenImage("OCR/OCR_candidate.png","png")
        # Secondly run tesseract.exe and process the image
        if _platform == "win32":             
            args = ('OCR/tesseract.exe', 'OCR/OCR_candidate.png', 'OCR/out', 'nobatch', 'letters')  
        elif _platform == "linux" or _platform == "linux2":
            args = ('/usr/bin/wine', 'OCR/tesseract.exe', 'OCR/OCR_candidate.png', 'OCR/out', 'nobatch', 'letters')
             
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        popen.wait()
        output = popen.stdout.read()
            
        # Lastly open and read the prepared recognized string
        f = open('OCR/out.txt')
        finalString = f.readline()
        f.close()
        return finalString

    def __boldenImage(self,imagename,imageext):
        img = Image.open(imagename)
        img = img.convert("RGBA")
        pixdata = img.load()

        for y in xrange(img.size[1]):
            for x in xrange(img.size[0]):
                if pixdata[x, y][0] < 90:
                    pixdata[x, y] = (0, 0, 0, 255)

        for y in xrange(img.size[1]):
            for x in xrange(img.size[0]):
                if pixdata[x, y][1] < 136:
                    pixdata[x, y] = (0, 0, 0, 255)

        for y in xrange(img.size[1]):
            for x in xrange(img.size[0]):
                if pixdata[x, y][2] > 0:
                    pixdata[x, y] = (255, 255, 255, 255)

        img.save(imagename, imageext)

