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
        self.infiltrator.process('../img/model/DSC_0486.jpg')

    def test2(self):
        self.infiltrator.process('../img/model/P1030325.jpg')

    def test3(self):
        self.infiltrator.process('../img/model/P1030292.jpg')

    def test4(self):
        self.infiltrator.process('../img/model/P1030332.jpg')

    # TODO add some bulk tests


