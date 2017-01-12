# -*- coding: utf-8 -*-

import unittest
import pandas as pd
from pyStratLib.analyzer.factor.norm import winsorize
from pyStratLib.analyzer.factor.norm import standardize
from pyStratLib.analyzer.factor.norm import getIndustryMatrix
from pyStratLib.analyzer.factor.norm import neutralize
from pyStratLib.analyzer.factor.norm import normalize


class TestNorm(unittest.TestCase):
    def setUp(self):
        index = ['000001.SZ', '000002.SZ', '000003.SZ', '000004.SZ', '000005.SZ', '000006.SZ', '000007.SZ', '000008.SZ',
                 '000009.SZ','000010.SZ']
        factor = [24,             1.0,        1.1,        0.8,        0.5,        1.2,        -1.0,        -2,        1.0,
                  0.5 ]
        industry =['801190.SI', '801190.SI', '801200.SI', '801200.SI','801200.SI', '801200.SI', '801200.SI', '801200.SI',
                   '801200.SI', '801200.SI']
        cap = [1.0,               1.0,        1.0,        1.0,        1.0,        1.0,        1.0,        1.0,        1.0,
               1.0 ]
        factor = pd.Series(factor, index=index)
        industry1 = pd.Series(industry, index=index)
        industry2 = pd.Series(industry, index=['000001.SZ', '000002.SZ', '100003.SZ', '000004.SZ', '000005.SZ', '000006.SZ',
                                              '000007.SZ','000008.SZ','000009.SZ','000010.SZ'])
        cap = pd.Series(cap, index=index)
        self.data = {'factor': factor,
                     'industry1': industry1,
                     'industry2': industry2,
                     'cap': cap}

    def testWinsorize(self):
        factor = self.data['factor']
        calculated = winsorize(factor, nb_std_or_quantile=3)
        expected = pd.Series([23.5572063591, 1.0, 1.1, 0.8, 0.5, 1.2, -1.0, -2.0, 1.0, 0.5],
                             index=['000001.SZ', '000002.SZ', '000003.SZ', '000004.SZ', '000005.SZ', '000006.SZ',
                                    '000007.SZ', '000008.SZ', '000009.SZ','000010.SZ'])
        pd.util.testing.assert_series_equal(calculated, expected)

        calculated = winsorize(factor, nb_std_or_quantile=[0.025, 0.975])
        expected = pd.Series([18.87, 1.0, 1.1, 0.8, 0.5, 1.2, -1.0, -1.775, 1.0, 0.5],
                             index=['000001.SZ', '000002.SZ', '000003.SZ', '000004.SZ', '000005.SZ', '000006.SZ',
                                    '000007.SZ', '000008.SZ', '000009.SZ','000010.SZ'])
        pd.util.testing.assert_series_equal(calculated, expected)

    def testStandardize(self):
        factor = self.data['factor']
        calculated = standardize(factor)
        expected = pd.Series([2.81897066159, -0.226418028714, -0.213177208321, -0.252899669499, -0.292622130677,
                              -0.199936387929, -0.491234436567, -0.623642640493, -0.226418028714, -0.292622130677],
                             index=['000001.SZ', '000002.SZ', '000003.SZ', '000004.SZ', '000005.SZ', '000006.SZ',
                                    '000007.SZ', '000008.SZ', '000009.SZ','000010.SZ'])
        pd.util.testing.assert_series_equal(calculated, expected)


