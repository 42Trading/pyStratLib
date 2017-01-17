# -*- coding: utf-8 -*-

import pandas as pd
from pyStratLib.analyzer.benchmark.benchmark import Benchmark
from pyStratLib.analyzer.factor.cleanData import getMultiIndexData



class Selector(object):
    def __init__(self, secScore, nbSecSelected=100, industry=None, benchmark=None, saveFile=False):
        self.__secScore = secScore
        self.__secScore.sort_values(ascending=False, inplace=True)
        self.__nbSecSelected = nbSecSelected
        self.__industry = industry
        self.__benchmark = benchmark
        self.__saveFile = saveFile

    def selectSecIDNonIndustryNeutral(self):
        ret = self.__secScore.iloc[:self.__nbSecSelected]
        return ret

    def selectedSecIDIndustryNeutral(self):

        return



