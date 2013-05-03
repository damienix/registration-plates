import os
from pytesser import *

def checkNameEqual(image,expectedResult):
    return expectedResult == image_to_string(image)
    

if __name__=='__main__':

    for files in os.listdir("./TabRejestracyjne"):
        if files.endswith(".png"):
            image = Image.open("./TabRejestracyjne/"+files)   
            print files + " " + image_to_string(image) 
