# -*- coding: utf-8 -*-
import pandas as pd
from pyStratLib.analyzer.factor.cleanData import getUniverseSingleFactor
from pyStratLib.analyzer.factor.cleanData import adjustFactorDate
from pyStratLib.utils.dateutils import getPosAdjDate


_factorPathDict = {
    'PRTYOY': ['..//..//data//factor//ProfitYoY.csv', 'q'],  # 净利润同比增长率,季度频率 - alpha因子
    'TRN': ['..//..//data//factor//Turnover.csv', 'm'],  # 月度换手率,月度频率 - alpha因子
    'ROE': ['..//..//data//factor//ROE.csv', 'q'],  # 净资产收益率,季度频率 -- 分层因子
    'CAP': ['..//..//data//factor//MktCap.csv', 'm'],  # 总市值,月度频率 -- 分层因子
    'RETURN': ['..//..//data//return//monthlyReturn.csv', 'm']  # 收益,月度频率
}


def getDataDiv(saveCSVPath, numerator='NAV', denominator='CAP', freq='m'):
    """
    :param saveCSVPath: str, save path and name of divide result
    :param numerator: str, optional, name of the numerator factor
    :param denominator: str, optional, name of the denominator factor
    :param freq: str, optional, the frequency of the data
    :return: DataFrame, the divide result
    """
    def getNewFactorSeries(data, freq):
        ret = adjustFactorDate(data,
                                          data.index.levels[0][0],
                                          data.index.levels[0][-1],
                                          freq)
        ret.index.names = ['tradeDate', 'secID']
        return ret

    numeratorData = getUniverseSingleFactor(_factorPathDict[numerator][0])
    denominatorData = getUniverseSingleFactor(_factorPathDict[denominator][0])

    if _factorPathDict[numerator][1] == freq:
        numeratorDataAdj = numeratorData
    else:
        numeratorDataAdj = getNewFactorSeries(numeratorData, freq)

    if _factorPathDict[denominator][1] == freq:
        denominatorDataAdj = denominatorData
    else:
        denominatorDataAdj = getNewFactorSeries(denominatorData, freq)

    ret = numeratorDataAdj.divide(denominatorDataAdj, axis='index')
    ret.to_csv(saveCSVPath)
    return ret


class FactorLoader(object):
    def __init__(self, startDate, endDate, factorNames, freq='m'):
        self.__startDate = startDate
        self.__endDate = endDate
        self.__factorNames = factorNames
        self.__freq = freq
        self.__tiaocangDate = []
        self.__nbFactor = len(factorNames)

    def getTiaoCangDate(self):
        return getPosAdjDate(self.__startDate, self.__endDate, freq=self.__freq)

    def getFactorData(self):
        ret = pd.Series()
        for name in self.__factorNames:
            pathToUse = _factorPathDict[name][0]
            originalFreq = _factorPathDict[name][1]
            if originalFreq <> self.__freq:
                factorRaw = getUniverseSingleFactor(pathToUse)
                factor = adjustFactorDate(factorRaw, self.__startDate, self.__endDate, self.__freq)
            else:
                factorRaw = getUniverseSingleFactor(pathToUse, IndexName=['tiaoCangDate', 'secID'])
                factorRaw = factorRaw.loc[factorRaw.index.get_level_values('tiaoCangDate') >= self.__startDate]
                factor = factorRaw.loc[factorRaw.index.get_level_values('tiaoCangDate') <= self.__endDate]
            factor.name = name
            ret[name] = factor
        return ret


if __name__ == "__main__":
    # factor = FactorLoader('2015-01-05', '2015-12-30', ['NAV', 'ROE', 'RETURN'])
    # ret = factor.getFactorData()
    # print ret['RETURN']
    print getDataDiv('BP.csv', 'NAV', 'CAP')
