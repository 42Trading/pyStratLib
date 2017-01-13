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


class DCAMAnalyzer(object):
    def __init__(self, layerFactor, alphaFactor, secReturn, tiaoCangDate, tiaoCangDateWindowSize=12):
        self.__layerFactor = layerFactor
        self.__layerFactorNames = [layerFactor.name for layerFactor in self.__layerFactor]
        self.__alphaFactor = alphaFactor
        self.__alphaFactorNames = [alphaFactor.name for alphaFactor in self.__alphaFactor]
        self.__secReturn = secReturn
        self.__tiaoCangDate = tiaoCangDate
        self.__startDate = str(Date.fromDateTime(self.__tiaoCangDate[0]))
        self.__endDate = str(Date.fromDateTime(self.__tiaoCangDate[-1]))
        self.__tiaoCangDateWindowSize = tiaoCangDateWindowSize
        pyFinAssert(len(self.__tiaoCangDate) > self.__tiaoCangDateWindowSize,
                    ValueError,
                    "length of tiaoCangDate must be larger than moving window size")


    def getSecGroup(self, layerFactor, date):
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

    def getSecReturn(self, secIDs, date):
        """
        :param secIDs: list of sec ids
        :param date: datetime, 调仓日
        :return: pd.Series, index = sec ID
        给定某一时间和股票代码列表, 返回前一个调仓日至当前调仓日的股票收益
        """
        data = getMultiIndexData(self.__secReturn, 'tiaoCangDate', date, 'secID', secIDs)
        data = data.reset_index().drop('tiaoCangDate', axis=1)
        data = data.set_index('secID')
        return data

    def getAlphaFactor(self, secIDs, date):
        """
        :param secIDs: list of sec ids
        :param date: datetime, 调仓日
        :return: pd.DataFrame, index = secIDs, col = [alpha factor]
        给定某一时间, 和股票代码列表, 返回alpha因子列表
        """
        ret = pd.DataFrame()
        for i in range(len(self.__alphaFactor)):
            data = getMultiIndexData(self.__alphaFactor[i], 'tiaoCangDate', date, 'secID', secIDs)
            data = data.reset_index().drop('tiaoCangDate', axis=1)
            data = data.set_index('secID')
            ret = pd.concat([ret, data], axis=1)
        ret.columns = self.__alphaFactorNames
        return ret

    def calcRankIC(self, layerFactor):
        """
        :param layerFactor: pd.Series, 分层因子
        :return: pd.DataFrame, index = tiaoCangDate, col = [alpha factor names]
        给定分层因子，计算每个调仓日对应的alpha因子IC
        """
        low = pd.DataFrame(index=self.__tiaoCangDate, columns=[self.__alphaFactorNames])
        high = pd.DataFrame(index=self.__tiaoCangDate, columns=[self.__alphaFactorNames])

        for j in range(0, len(self.__tiaoCangDate)-1):   #对时间做循环，得到每个时间点的rankIC
            date = self.__tiaoCangDate[j]
            nextDate = self.__tiaoCangDate[j+1]
            groupLow, groupHigh = self.getSecGroup(layerFactor, date)         #分组
            returnLow = self.getSecReturn(groupLow, date)
            returnHigh = self.getSecReturn(groupHigh, date)     #得到当期收益序列
            factorLow = self.getAlphaFactor(groupLow, nextDate)
            factorHigh = self.getAlphaFactor(groupHigh, nextDate)      #得到上期因子序列
            tableLow = pd.concat([returnLow, factorLow], axis=1)
            tableHigh = pd.concat([returnHigh, factorHigh], axis=1)
            for k in self.__alphaFactorNames:
                tmplow, _ = st.spearmanr(tableLow['RETURN'], tableLow[k])
                tmphigh, _ = st.spearmanr(tableHigh['RETURN'], tableHigh[k])
                low[k][j] = tmplow
                high[k][j] = tmphigh
        low = low.dropna()
        high = high.dropna()
        return low, high

    def getAnalysis(self, layerFactor=None):
        """
        :param layerFactor: pd.Series, layer factor series
        :return:  对给定情景因子分层后的股票组合进行的统计分析
        """
        if layerFactor is None:
            layerFactor = self.__layerFactor[0]
        low, high = self.calcRankIC(layerFactor)
        result = pd.DataFrame(columns=self.__alphaFactorNames, index=np.arange(12))
        for i in self.__alphaFactorNames:
            meanHigh = np.array(high[i]).mean()
            meanLow = np.array(low[i]).mean()
            stdHigh = np.array(high[i]).std()
            stdLow = np.array(low[i]).std()
            # 均值的t检验, 原假设为两个独立样本的均值相同
            t, p_t = st.ttest_ind(high[i], low[i], equal_var=False)
            # 方差的F检验，原假设为两个独立样本的方差相同
            F, p_F = st.levene(high[i], low[i])
            # 分布的K-S检验，原假设为两个独立样本是否来自同一个连续分布
            ks, p_ks = st.ks_2samp(high[i], low[i])
            result[i] = [meanHigh,meanLow,stdHigh,stdLow,meanHigh/stdHigh,meanLow/stdLow,t,p_t,F,p_F,ks,p_ks]

        result = result.T
        np.arrays = [['mean','mean','std','std','IR','IR','Two sample t test','Two sample t test','levene test','levene test','K-S test',
                      'K-S test'],
                     ['high','low','high','low','high','low','t','p_value','F','p_value','KS','p_value']]
        result.columns = pd.MultiIndex.from_tuples(zip(*np.arrays))
        ret = pd.concat([result], axis=1, keys = [layerFactor.name + '分层后因子表现     时间：' + self.__startDate + ' -- ' + self.__endDate])
        return ret

    def calcLayerFactorDistance(self, percentile):
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

    def getLayerFactorQuantileOnDate(self, date):
        """
        :param date: datetime, 调仓日
        :param layerFactor: multi index pd.Series, 情景分层因子
        :return: pd.DataFrame, index=secid, col = layerFactorNames
        """
        ret = pd.DataFrame()
        for layerFactor in self.__layerFactor:
            data = getMultiIndexData(layerFactor, 'tiaoCangDate', date)
            secIDs = data.index.get_level_values('secID').tolist()
            # 由高至低排序
            rank = data.rank(ascending=False)
            rank = rank.divide(len(secIDs))
            ret = pd.concat([ret, pd.Series(rank.values, index=secIDs)], axis=1, names=layerFactor.name)
        return ret

    def calcAlphaFactorWeightOnDate(self, date):
        """
        :param: date, datetime, tiaoCangDate
        :return:  pd.DataFrame,  index = [layerFactor], cols= [alpha factor name]
        给定调仓日，计算alpha因子的加权矩阵
        """
        if isinstance(date, basestring):
            date = Date.strptime(date).toDateTime()
            
        tiaoCangDateRange = self.__tiaoCangDate[self.__tiaoCangDate.index(date) - self.__tiaoCangDateWindowSize
                                                : self.__tiaoCangDate.index(date)]

        retLow = pd.DataFrame(columns=self.__alphaFactorNames)
        retHigh = pd.DataFrame(columns=self.__alphaFactorNames)

        for layerFactor in self.__layerFactor:
            low, high = self.calcRankIC(layerFactor)
            lowToUse = low.loc[tiaoCangDateRange]
            highToUse = high.loc[tiaoCangDateRange]
            weightLow = lowToUse.mean(axis=0) / lowToUse.std(axis=0)
            weightHigh = highToUse.mean(axis=0) / highToUse.std(axis=0)
            retLow.loc[layerFactor.name] = weightLow.values
            retHigh.loc[layerFactor.name] = weightHigh.values

        return retLow, retHigh

    def calcAlphaFactorRankOnDate(self, date):
        """
        :param secIDs, list, a group of sec ids
        :param date, str/datetime, tiaoCangDate
        :return:  pd.DataFrame,  index = [layerFactor, secID, low/high], index = layerfactor, col = alpha factor
        给定调仓日，计算secIDs的alpha因子的排位
        """
        ret = pd.DataFrame()
        if isinstance(date, basestring):
            date = Date.strptime(date).toDateTime()
        for layerFactor in self.__layerFactor:
            # 分层因子下股票分为两组
            groupLow, groupHigh = self.getSecGroup(layerFactor, date)
            # TODO check why length of factorLow <> groupLow
            factorLow = self.getAlphaFactor(groupLow, date)
            factorHigh = self.getAlphaFactor(groupHigh, date)
            # 由高到低排序
            factorLowRank = factorLow.rank(ascending=False, axis=0)
            factorHighRank = factorHigh.rank(ascending=False, axis=0)
            # multi index DataFrame
            secIDIndex = factorLowRank.index.union(factorHighRank.index)
            layerFactorIndex = [layerFactor.name] * len(secIDIndex)
            highLowIndex = ['low']*len(factorLowRank.index) + ['high']*len(factorHighRank.index)
            factorRankArray = pd.concat([factorLowRank, factorHighRank], axis=0).values
            index = pd.MultiIndex.from_arrays([secIDIndex, layerFactorIndex, highLowIndex], names=['secID', 'layerFactor', 'lowHigh'])
            alphaFactorRank = pd.DataFrame(factorRankArray, index=index, columns=self.__alphaFactorNames)
            # merge
            ret = pd.concat([ret, alphaFactorRank], axis=0)

        return ret

    def calcSecScoreOnDate(self, date):
        """
        :param secIDs: list, a group of sec ids
        :param date: datetime, tiaoCangDate
        :return: pd.Series, index = secID, cols = score
        给定调仓日,
        """
        alphaWightLow, alphaWeightHigh = self.calcAlphaFactorWeightOnDate(date)
        alphaFactorRank = self.calcAlphaFactorRankOnDate(date)
        layerFactorWeight = self.getLayerFactorQuantileOnDate(date)
        secIDs = layerFactorWeight.index.tolist()
        ret = pd.Series(index=secIDs, name='score')
        for secID in secIDs:
            # 提取secID对应的alphaFactorRank DataFrame, index = [layerFactor, high/low], col = alphaFactor
            factorRankMatrix = getMultiIndexData(alphaFactorRank, 'secID', secID)
            weightedRank = 0.0
            for layerFactor in factorRankMatrix.index.get_level_values('layerFactor'):
                factorRankOnLayerFactor = factorRankMatrix.loc[factorRankMatrix.index.get_level_values('layerFactor')==layerFactor]
                rank = factorRankOnLayerFactor.values
                lowHigh = factorRankOnLayerFactor.index.get_level_values('lowHigh')
                weight = alphaWightLow.loc[layerFactor].values if lowHigh == 'low' else alphaWeightHigh.loc[layerFactor].values
                weightedRank += np.dot(weight, rank) * layerFactorWeight.loc[secID]
            ret[secID] = weightedRank
        return ret

    def selectTopRankSecIDs(self, date=None, nbSecIDsSelected=50):
        """
        :param date: datetime, tiaoCangDate
        :param nbSecIDsSelected: int, optional,
        :return: list 返回股票代码列表
        """
        if date is None:
            date = self.__tiaoCangDate[self.__tiaoCangDateWindowSize]

        secScore = self.calcSecScoreOnDate(date)
        secScore.sort_values(ascending=False, inplace=True)
        secID = secScore.index.tolist()[:nbSecIDsSelected]
        return secID

if __name__ == "__main__":
    factor = FactorLoader('2006-01-05', '2015-12-31',
                          {'MV': FactorNormType.IndustryAndCapNeutral, # 分层因子
                           'BP_LF': FactorNormType.IndustryAndCapNeutral, # 分层因子
                           'EquityGrowth_YOY': FactorNormType.IndustryAndCapNeutral, # 分层因子
                           'ROE': FactorNormType.IndustryAndCapNeutral,   # 分层因子
                           'EP2_TTM': FactorNormType.IndustryAndCapNeutral, # alpha因子
                           'SP_TTM': FactorNormType.IndustryAndCapNeutral, # alpha 因子
                           'GP2Asset': FactorNormType.IndustryAndCapNeutral, # alpha因子
                           'PEG': FactorNormType.IndustryAndCapNeutral, # alpha因子
                           'ProfitGrowth_Qr_YOY': FactorNormType.IndustryAndCapNeutral, # alpha因子
                           'TO_adj': FactorNormType.IndustryAndCapNeutral, # alpha因子
                           'RETURN': FactorNormType.Null,
                           'INDUSTRY': FactorNormType.Null
                            })
    factorData = factor.getFactorData()
    analyzer = DCAMAnalyzer([factorData['MV']],
                            [factorData['BP_LF'], factorData['GP2Asset'], factorData['PEG'],
                             factorData['ProfitGrowth_Qr_YOY'], factorData['TO_adj']],
                            factorData['RETURN'],
                            factor.getTiaoCangDate())

    print analyzer.getAnalysis()
    print analyzer.calcAlphaFactorWeightOnDate('2012-01-31')




