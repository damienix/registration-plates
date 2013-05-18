import sys
from infiltrator import infiltrator
from tesseract import reader

__author__ = 'zbiki!'

inf = infiltrator.Infiltrator()
reader = reader.Reader()

compare = 'compare' in sys.argv
show = 'show' in sys.argv

cut_imgs = inf.process(sys.argv[1], compare=compare, show=show)
#reader.readText(cut_imgs)

inf.show_image()



