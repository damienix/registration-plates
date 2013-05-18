import sys
from infiltrator import infiltrator

__author__ = 'zbiki!'

inf = infiltrator.Infiltrator()

compare = 'compare' in sys.argv
show = 'show' in sys.argv

number = inf.process(sys.argv[1], compare=compare, show=show)
print number

inf.show_image()



