import os
import unittest
import cv2
from tesseract.reader import Reader

__author__ = 'damienix'


class BulkTest(unittest.TestCase):
    def setUp(self):
        self.reader = Reader()

    def test_all(self):
        PREFIX = "../img/plate/"

        failed = []

        for image in os.listdir(PREFIX):

            img = cv2.imread(PREFIX + image)
            number = self.reader.readText(img)

            if image != number:
                failed.append({'img': image, 'num': number})

        for fail in failed:
            print "%d : %s" % (fail['num'], fail['img'])
        self.assertEqual(len(failed), 0, "More than one plate found in some images.")


