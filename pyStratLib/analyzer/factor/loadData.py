# -*- coding: utf-8 -*-
import os
import zipfile
import pandas as pd
from pyStratLib.analyzer.factor.cleanData import adjustFactorDate
from pyStratLib.analyzer.factor.cleanData import getUniverseSingleFactor
from pyStratLib.utils.dateutils import getPosAdjDate

_factorPathDict = {
    'PRTYOY': ['..//..//data//factor//ProfitYoY.csv', 'q'],  # 净利润同比增长率, 季度频率 - alpha因子
    'TRN': ['..//..//data//factor//Turnover.csv', 'm'],  # 月度换手率, 月度频率 - alpha因子
    'TTM': ['..//..//data//factor//NetProfitTTM.csv', 'q'],  # 最近12个月净利润, 季度频率 -- alpha因子
    'BP': ['..//..//data//factor//BP_LF.csv', 'q'],  # 净资产除以总市值, 季度频率 -- 分层因子
    'ROE': ['..//..//data//factor//ROE.csv', 'q'],  # 净资产收益率, 季度频率 -- 分层因子
    'CAP': ['..//..//data//factor//MktCap.csv', 'm'],  # 总市值, 月度频率 -- 分层因子
    'EQTYGROTHYOY': ['..//..//data//factor//ProfitYoY.csv', 'q'],  # 净资产同比增长率, 季度频率 -- 分层因子
    'ROEYOY': ['..//..//data//factor//RoeYoY.csv', 'q'],  # ROE同比增长率, 季度频率 -- alpha测试因子
    'RETURN': ['..//..//data//return//monthlyReturn.csv', 'm'],  # 收益,月度频率
    'INDUSTRY': ['..//..//data//industry//codeSW.csv', 'm'],  # 申万行业分类,月度频率
    'EP2_TTM': ['..//..//data//factor//EP2_TTM.csv', 'q'],  # 剔除非经常性损益的过去12 个月净利润/总市值, 季度频率 -- alpha测试因子
    'GP2Asset': ['..//..//data//factor//GP2Asset.csv', 'q'],  # 销售毛利润/总资产, 季度频率 -- alpha测试因子
    'SP_TTM': ['..//..//data//factor//SP_TTM.csv', 'q'],  # 过去12 个月总营业收入/总市值, 季度频率 -- alpha测试因子
    'PEG': ['..//..//data//factor//PEG.csv', 'm'],  # 过去12 个月总营业收入/总市值, 月度频率 -- alpha测试因子
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
    def __init__(self, startDate, endDate, factorNames, freq='m', zipPath="..//..//data"):
        self.__startDate = startDate
        self.__endDate = endDate
        self.__factorNames = factorNames
        self.__freq = freq
        self.__tiaocangDate = []
        self.__nbFactor = len(factorNames)
        self.__zipPath = zipPath
        # 由于因子csv文件较大,所以默认存储为压缩格式的文件, 第一次使用时自动解压缩
        self._unzipCsvFiles(self.__zipPath)

    def _unzipCsvFiles(self, zipPath):
        """
        :param zipPath: str, 因子数据压缩包路径
        :return:
        解压缩因子数据压缩包，压缩包中尚未解压到目标文件夹中的文件将被解压
        """
        zipFile = zipfile.ZipFile(os.path.join(zipPath, "data.zip"), "r")
        for name in zipFile.namelist():
            name = name.replace('\\', '/')
            # 检查文件夹是否存在,新建尚未存在的文件夹
            if name.endswith("/"):
                extDir = os.path.join(zipPath, name)
                if not os.path.exists(extDir):
                    os.mkdir(extDir)
            # 检查数据文件是否存在，新建尚未存在的数据文件
            else:
                extFilename = os.path.join(zipPath, name)
                extDir = os.path.dirname(extFilename)
                if not os.path.exists(extDir):
                    os.mkdir(extDir)
                if not os.path.exists(extFilename):
                    outfile = open(extFilename, 'wb')
                    outfile.write(zipFile.read(name))
                    outfile.close()
        return

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
    factor = FactorLoader('2015-01-05', '2015-12-30', ['NAV', 'ROE', 'RETURN'])
    # ret = factor.getFactorData()
    # print ret['RETURN']
    # print getDataDiv('BP.csv', 'NAV', 'CAP')
