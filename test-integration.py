import os
import unittest
from infiltrator.infiltrator import Infiltrator
import sys

__author__ = 'damienix'


class BulkTest(unittest.TestCase):
    def setUp(self):
        self.infiltrator = Infiltrator()

    def test_all(self):
        PREFIX = os.path.join("img", "dzisiaj")
        
        failed = []
        recognized_count = 0
        not_recognized_count = 0
        all_count = 0        
        
        listDirectory = os.listdir(PREFIX)
        total = len(listDirectory)
        
        for image in listDirectory:
            all_count += 1
            print "------------------------------------------"
            print "Image %d/%d: %s" % (all_count, total, image)

            actual = os.path.splitext(image)[0]
            try:
                recognized = self.infiltrator.process(os.path.join(PREFIX, image), compare=False, show=False)
            except:
                recognized = None;
            if not recognized:
                not_recognized_count += 1
            elif actual != recognized:
                failed.append({'img': actual, 'n': recognized})
            else:
                recognized_count += 1
                

        print "=========================================="
        print "False positives:"
        for fail in failed:
            print 'Actual:     %s' % fail['img']
            print 'Recognized: %s' % fail['n']

        print "=========================================="
        print "Statistics:"
        print "  Total          : %d" % all_count
        print "  Correct        : %d" % recognized_count
        print "  Not recognized : %d" % not_recognized_count
        print "  Fail           : %d" % len(failed)
        print "  Error ratio    : %.2f" % (float(len(failed)) / all_count)
        print "  Success ratio  : %.2f" % (float(recognized_count) / all_count)
        self.assertEqual(len(failed), 0, "More than one plate found in some images.")

