# -*- coding: utf-8 -*-

import pandas as pd
from pyStratLib.analyzer.benchmark.benchmark import Benchmark
from pyStratLib.analyzer.factor.cleanData import getMultiIndexData
from PyFin.Utilities import pyFinAssert



class Selector(object):
    def __init__(self,
                 secScore,
                 industry,
                 nbSecSelected=100,
                 benchmark=None,
                 saveFile=False):
        """
        :param secScore: pd.DataFrame, index = secID, col = tiaoCangDate, value = score
        :param industry: pd.DataFrame, index = secID, col = tiaoCangDate, value = industry name
        :param nbSecSelected: int, optional, nb sec to be selected
        :param benchmark: Benchmark class object, optional
        :param saveFile: bool, optional, save result to csv or not
        :return:
        """
        self._secScore = secScore
        self._secScore.sort_values(ascending=False, inplace=True)
        self._industry = industry
        self._nbSecSelected = nbSecSelected
        self._benchmark = benchmark
        self._saveFile = saveFile
        self._tiaoCangDate = self._secScore.columns.values
        self._secSelected = None
        self._industryNeutral = True if self._benchmark is not None else False

    @property
    def secSelected(self):
        return self._secSelected

    @property
    def industryNeutral(self):
        return self._industryNeutral

    @industryNeutral.setter
    def industryNeutral(self, flag):
        pyFinAssert(isinstance(flag, bool), TypeError, "flag must be bool type variable")
        self.__industryNeutral = flag


    def secSelection(self):
        secScore = pd.concat([self._secScore, self._industry], join_axes=[self._secScore.index], axis=1)
        ret = pd.DataFrame()
        for date in secScore.index.get_level_values('tiaoCangDate'):
            secScoreOnDate = getMultiIndexData(secScore, 'tiaoCangDate', date)
            secScoreOnDate.sort_values(by='score', ascending=False, inplace=True)
            if self.__industryNeutral:
                nbSecByIndustry = self._benchmark.calcNbSecSelectedOnDate(date)
                #TODO implementation
            else:
                secScoreOnDate = secScoreOnDate[:self._nbSecSelected+1]
                ret = pd.concat([ret, secScoreOnDate], axis=0)
        return ret




