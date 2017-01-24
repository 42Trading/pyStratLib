# -*- coding: utf-8 -*-
#ref 动态情景多因子Alpha模型----因子选股系列研究之八，朱剑涛
#ref https://uqer.io/community/share/57ff3f9e228e5b3658fac3ed
import numpy as np
import pandas as pd
import scipy.stats as st
from pyStratLib.analyzer.factor.loadData import FactorLoader
from pyStratLib.analyzer.factor.cleanData import getMultiIndexData
from PyFin.Utilities import pyFinAssert
from PyFin.DateUtilities import Date
from pyStratLib.enums.factorNorm import FactorNormType
from pyStratLib.analyzer.factor.selector import Selector
from pyStratLib.analyzer.benchmark.benchmark import Benchmark

class DCAMAnalyzer(object):
    def __init__(self, layerFactor, alphaFactor, secReturn, tiaoCangDate, industryCode=None, tiaoCangDateWindowSize=12):
        self._layerFactor = layerFactor
        self._layerFactorNames = [layerFactor.name for layerFactor in self._layerFactor]
        self._alphaFactor = alphaFactor
        self._alphaFactorNames = [alphaFactor.name for alphaFactor in self._alphaFactor]
        self._secReturn = secReturn
        self._tiaoCangDate = tiaoCangDate
        self._industryCode = industryCode
        self._startDate = str(Date.fromDateTime(self.__tiaoCangDate[0]))
        self._endDate = str(Date.fromDateTime(self.__tiaoCangDate[-1]))
        self._tiaoCangDateWindowSize = tiaoCangDateWindowSize
        pyFinAssert(len(self.__tiaoCangDate) > self.__tiaoCangDateWindowSize,
                    ValueError,
                    "length of tiaoCangDate must be larger than moving window size")


    def _getSecGroup(self, layerFactor, date):
        """
        :param date: datetime, 调仓日
        :param layerFactor: multi index pd.Series, 情景分层因子
        :return: list
        给定某一时间，按分层因子layerFactor把股票分为数量相同的两组（大/小）
        """
        data = getMultiIndexData(layerFactor, 'tiaoCangDate', date)
        # 按分层因子值从小到大排序
        data.sort_values(ascending=True, inplace=True)
        secIDs = data.index.get_level_values('secID').tolist()
        # 分组,因子值小的哪一组股票为low,高的为high
        group_low = secIDs[:np.round(len(data))/2]
        group_high = secIDs[np.round(len(data))/2:]
        return group_low, group_high

    def _getSecReturn(self, secIDs, date):
        """
        :param secIDs: list of sec ids
        :param date: datetime, 调仓日
        :return: pd.Series, index = sec ID
        给定某一时间和股票代码列表, 返回前一个调仓日至当前调仓日的股票收益
        """
        data = getMultiIndexData(self._secReturn, 'tiaoCangDate', date, 'secID', secIDs)
        data = data.reset_index().drop('tiaoCangDate', axis=1)
        data = data.set_index('secID')
        return data

    def _getAlphaFactor(self, secIDs, date):
        """
        :param secIDs: list of sec ids
        :param date: datetime, 调仓日
        :return: pd.DataFrame, index = secIDs, col = [alpha factor]
        给定某一时间, 和股票代码列表, 返回alpha因子列表
        """
        ret = pd.DataFrame()
        for i in range(len(self._alphaFactor)):
            data = getMultiIndexData(self._alphaFactor[i], 'tiaoCangDate', date, 'secID', secIDs)
            data = data.reset_index().drop('tiaoCangDate', axis=1)
            data = data.set_index('secID')
            ret = pd.concat([ret, data], axis=1)
        ret.columns = self._alphaFactorNames
        return ret

    def _calcRankIC(self, layerFactor):
        """
        :param layerFactor: pd.Series, 分层因子
        :return: pd.DataFrame, index = tiaoCangDate, col = [alpha factor names]
        给定分层因子，计算每个调仓日对应的alpha因子IC
        """
        low = pd.DataFrame(index=self._tiaoCangDate, columns=[self._alphaFactorNames])
        high = pd.DataFrame(index=self._tiaoCangDate, columns=[self._alphaFactorNames])

        for j in range(0, len(self._tiaoCangDate)-1):   #对时间做循环，得到每个时间点的rankIC
            date = self._tiaoCangDate[j]
            nextDate = self._tiaoCangDate[j+1]
            groupLow, groupHigh = self._getSecGroup(layerFactor, date)         #分组
            returnLow = self._getSecReturn(groupLow, nextDate)
            returnHigh = self._getSecReturn(groupHigh, nextDate)     #得到当期收益序列
            factorLow = self._getAlphaFactor(groupLow, date)
            factorHigh = self._getAlphaFactor(groupHigh, date)      #得到上期因子序列
            tableLow = pd.concat([returnLow, factorLow], axis=1)
            tableHigh = pd.concat([returnHigh, factorHigh], axis=1)
            for k in self._alphaFactorNames:
                tmplow, _ = st.spearmanr(tableLow['RETURN'], tableLow[k])
                tmphigh, _ = st.spearmanr(tableHigh['RETURN'], tableHigh[k])
                low[k][j] = tmplow
                high[k][j] = tmphigh
        low = low.dropna()
        high = high.dropna()
        return low, high

    def getAnalysis(self, layerFactorName=None, saveFile=False):
        """
        :param layerFactor: pd.Series, layer factor series
        :return:  对给定情景因子分层后的股票组合进行的统计分析
        """
        if layerFactorName is None:
            layerFactor = self._layerFactor[0]
        else:
            layerFactor = self._layerFactor[self._layerFactorNames.index(layerFactorName)]
        low, high = self._calcRankIC(layerFactor)
        result = pd.DataFrame(columns=self._alphaFactorNames, index=np.arange(12))
        for i in self._alphaFactorNames:
            meanLow = np.array(low[i]).mean()
            meanHigh = np.array(high[i]).mean()
            stdLow = np.array(low[i]).std()
            stdHigh = np.array(high[i]).std()
            # 均值的t检验, 原假设为两个独立样本的均值相同
            t, p_t = st.ttest_ind( low[i], high[i], equal_var=False)
            # 方差的F检验，原假设为两个独立样本的方差相同
            F, p_F = st.levene(low[i], high[i])
            # 分布的K-S检验，原假设为两个独立样本是否来自同一个连续分布
            ks, p_ks = st.ks_2samp(low[i], high[i])
            result[i] = [meanLow, meanHigh, stdLow, stdHigh,
                         meanLow/stdLow, meanHigh/stdHigh, t, p_t, F, p_F, ks, p_ks]

        result = result.T
        np.arrays = [['mean','mean','std','std','IR','IR','Two sample t test','Two sample t test','levene test','levene test','K-S test',
                      'K-S test'],
                     ['low','high','low','high','low','high','t','p_value','F','p_value','KS','p_value']]
        result.columns = pd.MultiIndex.from_tuples(zip(*np.arrays))
        ret = pd.concat([result], axis=1, keys = [layerFactor.name + '分层后因子表现     时间：' + self._startDate + ' -- ' + self._endDate])
        if saveFile:
            ret.to_csv('analysis.csv')
        return ret

    def _calcLayerFactorDistance(self, percentile):
        """
        :param percentile: 个股在分层因子下的分位数
        :return: float, 个股的分层因子上的属性量化分数
        """
        if percentile >= 85:
            return 9
        elif 50 <= percentile < 85:
            return 9 * (percentile/35.0 - 50.0/35.0) ** 0.7
        elif 15 <= percentile < 50:
            return -9 * (percentile/35.0 - 50.0/35.0) ** 0.7
        else:
            return -9

    def _caclLayerFactorQuantileOnDate(self, date):
        """
        :param date: datetime, 调仓日
        :param layerFactor: multi index pd.Series, 情景分层因子
        :return: pd.DataFrame, index=secid, col = layerFactorNames
        """
        ret = pd.DataFrame()
        for layerFactor in self._layerFactor:
            data = getMultiIndexData(layerFactor, 'tiaoCangDate', date)
            secIDs = data.index.get_level_values('secID').tolist()
            # 由高至低排序
            rank = data.rank(ascending=False)
            rank = rank.divide(len(secIDs))
            ret = pd.concat([ret, pd.Series(rank.values, index=secIDs)], axis=1)
        ret.columns = self._layerFactorNames
        return ret

    def _calcAlphaFactorWeightOnDate(self, date):
        """
        :param: date, datetime, tiaoCangDate
        :return:  pd.DataFrame,  index = [layerFactor], cols= [alpha factor name]
        给定调仓日，计算alpha因子的加权矩阵
        """
        if isinstance(date, basestring):
            date = Date.strptime(date).toDateTime()
            
        tiaoCangDateRange = self._tiaoCangDate[self._tiaoCangDate.index(date) - self._tiaoCangDateWindowSize
                                                : self._tiaoCangDate.index(date)]

        retLow = pd.DataFrame(columns=self._alphaFactorNames)
        retHigh = pd.DataFrame(columns=self._alphaFactorNames)

        for layerFactor in self._layerFactor:
            low, high = self._calcRankIC(layerFactor)
            lowToUse = low.loc[tiaoCangDateRange]
            highToUse = high.loc[tiaoCangDateRange]
            weightLow = lowToUse.mean(axis=0) / lowToUse.std(axis=0)
            weightHigh = highToUse.mean(axis=0) / highToUse.std(axis=0)
            retLow.loc[layerFactor.name] = weightLow.values
            retHigh.loc[layerFactor.name] = weightHigh.values

        return retLow, retHigh

    def _calcAlphaFactorRankOnDate(self, date):
        """
        :param secIDs, list, a group of sec ids
        :param date, str/datetime, tiaoCangDate
        :return:  pd.DataFrame,  index = [layerFactor, secID, low/high], index = layerfactor, col = alpha factor
        给定调仓日，计算secIDs的alpha因子的排位
        """
        ret = pd.DataFrame()
        if isinstance(date, basestring):
            date = Date.strptime(date).toDateTime()
        for layerFactor in self._layerFactor:
            # 分层因子下股票分为两组
            groupLow, groupHigh = self._getSecGroup(layerFactor, date)
            # TODO check why length of factorLow <> groupLow
            factorLow = self._getAlphaFactor(groupLow, date)
            factorHigh = self._getAlphaFactor(groupHigh, date)
            # 由低到高排序
            factorLowRank = factorLow.rank(ascending=True, axis=0)
            factorHighRank = factorHigh.rank(ascending=True, axis=0)
            # multi index DataFrame
            secIDIndex = factorLowRank.index.union(factorHighRank.index)
            layerFactorIndex = [layerFactor.name] * len(secIDIndex)
            highLowIndex = ['low']*len(factorLowRank.index) + ['high']*len(factorHighRank.index)
            factorRankArray = pd.concat([factorLowRank, factorHighRank], axis=0).values
            index = pd.MultiIndex.from_arrays([secIDIndex, layerFactorIndex, highLowIndex], names=['secID', 'layerFactor', 'lowHigh'])
            alphaFactorRank = pd.DataFrame(factorRankArray, index=index, columns=self._alphaFactorNames)
            # merge
            ret = pd.concat([ret, alphaFactorRank], axis=0)
        ret.fillna(0, inplace=True)
        return ret

    def _calcSecScoreOnDate(self, date):
        """
        :param secIDs: list, a group of sec ids
        :param date: datetime, tiaoCangDate
        :return: pd.Series, index = secID, cols = score, industry
        给定调仓日, 返回股票打分列表
        """
        alphaWeightLow, alphaWeightHigh = self._calcAlphaFactorWeightOnDate(date)
        alphaFactorRank = self._calcAlphaFactorRankOnDate(date)
        layerFactorQuantile = self._caclLayerFactorQuantileOnDate(date)
        secIDs = layerFactorQuantile.index.tolist()
        ret = pd.Series(index=secIDs, name=date)
        for secID in secIDs:
            # 提取secID对应的alphaFactorRank DataFrame, index = [layerFactor, high/low], col = alphaFactor
            factorRankMatrix = getMultiIndexData(alphaFactorRank, 'secID', secID)
            weightedRank = 0.0
            for layerFactor in factorRankMatrix.index.get_level_values('layerFactor'):
                factorRankOnLayerFactor = factorRankMatrix.loc[factorRankMatrix.index.get_level_values('layerFactor')==layerFactor]
                rank = factorRankOnLayerFactor.values.flatten()
                lowHigh = factorRankOnLayerFactor.index.get_level_values('lowHigh')
                weight = alphaWeightLow.loc[layerFactor].values if lowHigh == 'low' else alphaWeightHigh.loc[layerFactor].values
                layerFactorQuantileToUse = layerFactorQuantile[layerFactor][secID]
                weightedRank += np.dot(weight, rank) * self._calcLayerFactorDistance(layerFactorQuantileToUse)
            ret[secID] = weightedRank

        return ret

    def calcSecScore(self):
        """
        :param self:
        :return: pd.Series, index = [tiaoCangDate, secID], value = score
        返回所有调仓日的股票打分列表
        """
        dateIndex = []
        secIDIndex = []
        secScoreValue = []
        for date in self._tiaoCangDate[self._tiaoCangDateWindowSize:]:
            secScore = self._calcSecScoreOnDate(date)
            dateIndex += [date] * len(secScore.values)
            secIDIndex += secScore.index.tolist()
            secScoreValue += secScore.values.tolist()

        index = pd.MultiIndex.from_arrays([dateIndex, secIDIndex], names=['tiaoCangDate','secID'])
        ret = pd.Series(secScoreValue, index=index, name='score')
        return ret


def DCAMSelector(analyzeFactorOnly=False):

    factor = FactorLoader('2006-10-05', '2016-10-31',
                          {'MV': FactorNormType.Null, # 分层因子
                           'BP_LF': FactorNormType.IndustryAndCapNeutral, # 分层因子
                           'EquityGrowth_YOY': FactorNormType.IndustryAndCapNeutral, # 分层因子
                           'ROE': FactorNormType.IndustryAndCapNeutral,   # 分层因子
                           'EP2_TTM': FactorNormType.IndustryAndCapNeutral, # alpha因子
                           #'SP_TTM': FactorNormType.IndustryAndCapNeutral, # alpha 因子
                           'GP2Asset': FactorNormType.IndustryAndCapNeutral, # alpha因子
                           'PEG': FactorNormType.IndustryAndCapNeutral, # alpha因子
                           'ProfitGrowth_Qr_YOY': FactorNormType.IndustryAndCapNeutral, # alpha因子
                           'TO_adj': FactorNormType.IndustryAndCapNeutral, # alpha因子
                           'RETURN': FactorNormType.IndustryAndCapNeutral,
                           'INDUSTRY': FactorNormType.Null,
                           'IND_WGT': FactorNormType.Null
                            })
    factorData = factor.getNormFactorData()

    analyzer = DCAMAnalyzer(layerFactor=[factorData['MV']],
                            alphaFactor=[factorData['ROE'], factorData['EP2_TTM'], factorData['GP2Asset'], factorData['PEG'],
                             factorData['ProfitGrowth_Qr_YOY'], factorData['TO_adj']],
                            secReturn=factorData['RETURN'],
                            tiaoCangDate=factor.getTiaoCangDate())

    if analyzeFactorOnly:
        print analyzer.getAnalysis()
    else:
        secScore = analyzer.calcSecScore()

        benchmark = Benchmark(industryWeight=factorData['IND_WGT'])
        selector = Selector(secScore=secScore,
                            industry=factorData['INDUSTRY'],
                            benchmark=benchmark)
        selector.industryNeutral = False
        selector.secSelection()
        print selector.secSelected




if __name__ == "__main__":
    DCAMSelector()

