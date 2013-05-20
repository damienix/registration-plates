import os
from pytesser import *


def checkNameEqual(image, expectedResult):
    return expectedResult == image_to_string(image)


if __name__ == '__main__':

    for file in os.listdir("../img/plate"):
        if file.endswith(".png"):
            image = Image.open("../img/plate/" + file)
            print file + " " + image_to_string(image)
