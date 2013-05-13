import cv2
import subprocess
from sys import platform as _platform

class Reader:
    def readText(self, cut_imgs):
        for img in cut_imgs:
            print "Read plate:", self.__OCR_image(img)
            
    def __OCR_image(self, img):
        if _platform == "win32":
            params = list()
            params.append(cv2.cv.CV_IMWRITE_PNG_COMPRESSION)
            params.append(8)
            cv2.imwrite("OCR/OCR_candidate.png", img, params)
            
            args = ('OCR/tesseract.exe', 'OCR/OCR_candidate.png', 'OCR/out', 'nobatch', 'letters')
                    
            #Or just:
            #args = "bin/bar -c somefile.xml -d text.txt -r aString -f anotherString".split()
            popen = subprocess.Popen(args, stdout=subprocess.PIPE)
            popen.wait()
            output = popen.stdout.read()
            
            f = open('OCR/out.txt')
            finalString = f.readline()
            f.close()
            
            return finalString
            
        elif _platform == "linux" or _platform == "linux2":
            print "TODO"
            
