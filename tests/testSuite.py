# -*- coding: utf-8 -*-

import os
import sys

thisFilePath = os.path.abspath(__file__)

sys.path.append(os.path.sep.join(thisFilePath.split(os.path.sep)[:-2]))

import unittest
import pyStratLib.tests.analyzer as analyzer
import pyStratLib.tests.maths as maths
import pyStratLib.tests.utils as utils


def test():
    print('Python ' + sys.version)
    suite = unittest.TestSuite()

    tests = unittest.TestLoader().loadTestsFromTestCase(analyzer.TestCleanData)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(maths.TestMatrix)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(maths.TestStats)
    suite.addTests(tests)
    tests = unittest.TestLoader().loadTestsFromTestCase(utils.TestDateUtils)
    suite.addTests(tests)

    res = unittest.TextTestRunner(verbosity=3).run(suite)
    if len(res.errors) >= 1 or len(res.failures) >= 1:
        sys.exit(-1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    test()
