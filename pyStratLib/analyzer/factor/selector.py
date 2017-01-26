# -*- coding: utf-8 -*-

import pandas as pd
from PyFin.Utilities import pyFinAssert
from pyStratLib.analyzer.benchmark.benchmark import Benchmark
from pyStratLib.analyzer.factor.cleanData import getMultiIndexData
from pyStratLib.utils.misc import top


class Selector(object):
    def __init__(self,
                 secScore,
                 industry=None,
                 nbSecSelected=100,
                 benchmark=None,
                 saveFile=False,
                 useIndustryName=True):
        """
        :param secScore: pd.Series, index = [tiaoCangDate, secID], value = score
        :param industry: pd.Series, optional, index = [tiaoCangDate, secID], value = industry name
        :param nbSecSelected: int, optional, nb sec to be selected
        :param benchmark: Benchmark class object, optional
        :param saveFile: bool, optional, save result to csv or not
        :param useIndustryName: bool, optional, whether to use name instead of code in return dataframe
        :return:
        """
        self._secScore = secScore
        self._secScore.sort_values(ascending=False, inplace=True)
        self._industry = industry
        self._nbSecSelected = nbSecSelected
        self._benchmark = benchmark
        self._saveFile = saveFile
        self._secSelected = None
        self._tiaoCangDate = list(set(self._secScore.index.get_level_values('tiaoCangDate').tolist()))
        self._industryNeutral = True
        self._useIndustryName = useIndustryName

    @property
    def secSelected(self):
        return self._secSelected

    @property
    def industryNeutral(self):
        return self._industryNeutral

    @industryNeutral.setter
    def industryNeutral(self, flag):
        pyFinAssert(isinstance(flag, bool), TypeError, "flag must be bool type variable")
        self._industryNeutral = flag

    def secSelection(self):
        if self._industry is not None:
            secScore = pd.concat([self._secScore, self._industry], join_axes=[self._secScore.index], axis=1)
        ret = pd.DataFrame()
        for date in self._tiaoCangDate:
            secScoreOnDate = getMultiIndexData(secScore, 'tiaoCangDate', date)
            secScoreOnDate.sort_values(by='score', ascending=False, inplace=True)
            if self._industryNeutral:
                pyFinAssert(self._industry is not None, ValueError, "industry information missing ")
                nbSecByIndustry = self._benchmark.calcNbSecSelectedOnDate(date)
                for name, group in secScoreOnDate.groupby(self._industry.name):
                    largestScore = top(group, column='score', n=nbSecByIndustry[name])
                    ret = pd.concat([ret, largestScore], axis=0)
            else:
                secScoreOnDate = secScoreOnDate[:self._nbSecSelected + 1]
                ret = pd.concat([ret, secScoreOnDate], axis=0)

        if self._useIndustryName:
            industryName = Benchmark.mapIndustryCodeToName(ret[self._industry.name])
            ret = ret['score']
            ret = pd.concat([ret, industryName], join_axes=[ret.index], axis=1)

        self._secSelected = ret

        return
