import sys
from infiltrator import infiltrator
from tesseract import reader

__author__ = 'zbiki!'

inf = infiltrator.Infiltrator()
reader = reader.Reader()

cut_imgs = inf.process(sys.argv[1], len(sys.argv) > 2, show=True)
reader.readText(cut_imgs)



