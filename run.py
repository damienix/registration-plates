import sys
from scripts import infiltrator

__author__ = 'hauron'


inf = infiltrator.Infiltrator()

inf.process(sys.argv[1])
