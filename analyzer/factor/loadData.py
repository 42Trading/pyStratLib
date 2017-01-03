# -*- coding: utf-8 -*-
import pandas as pd

import cleanData
from utils import dateutils

_factorPathDict = {
    'BPS': ['..//..//data//factor//BPS.csv', 'q'],  # 每股净资产,季度频率,
    'OPR': ['..//..//data//factor//OperRev.csv', 'q'],  # 营业利润,季度频率
    'PRTYOY': ['..//..//data//factor//ProfitYoY.csv', 'q'],  # 净利润同比增长率,季度频率
    'TRN': ['..//..//data//factor//Turnover.csv', 'm'],  # 月度换手率,月度频率
    'ROEYOY': ['..//..//data//factor//RoeYoY.csv', 'q'],  # 净利润增长率（季度同比）,季度频率
    'NAV': ['..//..//data//factor//NetAsset.csv', 'm'],  # 当日净资产,月度频率
    'ROE': ['..//..//data//factor//ROE.csv', 'q'],  # 净资产收益率,季度频率
    'PE': ['..//..//data//factor//PE_TTM.csv', 'm'],  # 市盈率,月度频率
    'TTM': ['..//..//data//factor//TTM.csv', 'q'],  # 销售毛利率,季度频率
    'CAP': ['..//..//data//factor//MktCap.csv', 'm'],  # 总市值,月度频率
    'RETURN': ['..//..//data//return//monthlyReturn.csv', 'm']  # 收益,月度频率
}


def getDataDiv(saveCSVPath, numerator='NAV', denominator='CAP', freq='m'):
    numeratorData = pd.read_csv(_factorPathDict[numerator][0])
    denominatorData = pd.read_csv(_factorPathDict[denominator][0])
    numeratorDataAdj = numeratorData if _factorPathDict[numerator][1] == freq else \
        cleanData.adjustFactorDate(numeratorData, numeratorData.iloc[0,0], numeratorData.iloc[-1,0], freq)
    denominatorDataAdj = denominatorData if _factorPathDict[denominator][1] == freq else \
        cleanData.adjustFactorDate(denominatorData, denominatorData.iloc[0,0], denominatorData.iloc[-1,0], freq)

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
        return dateutils.getPosAdjDate(self.__startDate, self.__endDate, freq=self.__freq)

    def getFactorData(self):
        ret = pd.Series()
        for name in self.__factorNames:
            pathToUse = _factorPathDict[name][0]
            originalFreq = _factorPathDict[name][1]
            if originalFreq <> self.__freq:
                factorRaw = cleanData.getUniverseSingleFactor(pathToUse)
                factor = cleanData.adjustFactorDate(factorRaw, self.__startDate, self.__endDate, self.__freq)
            else:
                factorRaw = cleanData.getUniverseSingleFactor(pathToUse, IndexName=['tiaoCangDate', 'secID'])
                factorRaw = factorRaw.loc[factorRaw.index.get_level_values('tiaoCangDate') >= self.__startDate]
                factor = factorRaw.loc[factorRaw.index.get_level_values('tiaoCangDate') <= self.__endDate]
            factor.name = name
            ret[name] = factor
        return ret


if __name__ == "__main__":
    #factor = FactorLoader('2015-01-05', '2015-12-30', ['NAV', 'ROE', 'RETURN'])
    #ret = factor.getFactorData()
    #print ret['RETURN']
    print getDataDiv('BP.csv', 'NAV', 'CAP')
