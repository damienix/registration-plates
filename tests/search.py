import unittest

import os


def load(filename):
    fullname = os.path.dirname(__file__)
    fullname += '../img/' + filename + '.jpg'
    file = open(fullname)
    image = file.read()
    return image


class TestSearch(unittest.TestCase):
    def setUp(self):
        pass



