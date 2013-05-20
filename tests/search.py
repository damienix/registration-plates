import unittest
import os

from infiltrator.infiltrator import Infiltrator


def load(filename):
    fullname = os.path.dirname(__file__)
    fullname += '../img/' + filename + '.jpg'
    file = open(fullname)
    image = file.read()
    return image


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.infiltrator = Infiltrator()

    def test1(self):
        self.infiltrator.process('../img/model/ZGR55XY.jpg')

    def test2(self):
        self.infiltrator.process('../img/model/GD983CV.jpg')

    def test3(self):
        self.infiltrator.process('../img/model/DG62121.jpg')

    def test4(self):
        self.infiltrator.process('../img/model/GBYPC76.jpg')

        # TODO add some bulk tests


class BulkTest(unittest.TestCase):
    def setUp(self):
        self.infiltrator = Infiltrator()

    def test_all(self):
        PREFIX = "../img/model/"

        failed = []

        for image in os.listdir(PREFIX):
            found_num = len(self.infiltrator.process(PREFIX + image))
            if found_num > 1:
                failed.append({'img': image, 'n': found_num})

        for fail in failed:
            print "%d : %s" % (fail['n'], fail['img'])
        self.assertEqual(len(failed), 0, "More than one plate found in some images.")


