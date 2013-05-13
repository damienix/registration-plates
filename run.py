import sys
from infiltrator import infiltrator


__author__ = 'hauron'

inf = infiltrator.Infiltrator()

inf.process(sys.argv[1], len(sys.argv)>2)
