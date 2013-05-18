import sys
from infiltrator import infiltrator
from tesseract import reader

__author__ = 'zbiki!'

inf = infiltrator.Infiltrator()
reader = reader.Reader()

compare = 'compare' in sys.argv
show = 'show' in sys.argv

number = inf.process(sys.argv[1], compare=compare, show=show)
print number

inf.show_image()



