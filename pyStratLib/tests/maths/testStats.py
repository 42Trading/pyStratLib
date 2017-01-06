# -*- coding: utf-8 -*-
import unittest
from pyStratLib.maths.stats import runningSum


class TestStats(unittest.TestCase):
    def testRunningSum(self):
        calculated = list(runningSum([1, 2, 3, 4], 3))
        expected = [6, 9]
        self.assertListEqual(calculated, expected, "Calculated Running Sum is wrong")

        calculated = list(runningSum([1, 2, 3, 4], 2))
        expected = [3, 5, 7]
        self.assertListEqual(calculated, expected, "Calculated Running Sum is wrong")
