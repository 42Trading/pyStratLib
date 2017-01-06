# -*- coding: utf-8 -*-
#ref 动态情景多因子Alpha模型----因子选股系列研究之八，朱剑涛
#ref https://uqer.io/community/share/57ff3f9e228e5b3658fac3ed
import numpy as np
import pandas as pd
import scipy.stats as st
from loadData import FactorLoader
from cleanData import getMultiIndexData
from PyFin.Utilities import pyFinAssert

class DCAMAnalyzer(object):
    def __init__(self, layerFactor, alphaFactor, secReturn, tiaoCangDate, startDate='', endDate='', tiaoCangDateWindowSize=12):
        self.__layerFactor = layerFactor
        self.__layerFactorNames = [layerFactor.name for layerFactor in self.__layerFactor]
        self.__alphaFactor = alphaFactor
        self.__alphaFactorNames = [alphaFactor.name for alphaFactor in self.__alphaFactor]
        self.__secReturn = secReturn
        self.__tiaoCangDate = tiaoCangDate
        self.__startDate = startDate
        self.__endDate = endDate
        self.__tiaoCangDateWindowSize = tiaoCangDateWindowSize

    # 给定某一时间，按分层因子layerFactor把股票分为数量相同的两组（大小）
    def getGroup(self, date, layerFactor):
        data = getMultiIndexData(layerFactor, 'tiaoCangDate', date)
        data.sort_values(ascending=True, inplace=True)     #按分层因子值从小到大排序
        secIDs = data.index.get_level_values('secID').tolist()
        group_low = secIDs[:np.round(len(data))/2]        #分组,因子值小的哪一组股票为low,高的为high
        group_high = secIDs[np.round(len(data))/2:]
        return group_low, group_high

    # 给定某一时间，和股票代码列表，返回收益序列
    def getReturn(self, secIDs, date):
        data = getMultiIndexData(self.__secReturn, 'tiaoCangDate', date, 'secID', secIDs)
        return data

    # 给定某一时间, 和股票代码列表, 返回因子列表
    def getAlphaFactor(self, secIDs, date):
        ret = pd.Series()
        for i in range(len(self.__alphaFactor)):
            data = getMultiIndexData(self.__alphaFactor[i], 'tiaoCangDate', date, 'secID', secIDs)
            ret[data.name] = data
        return ret

    # 对收益数据和因子数据做一个concat,避免因子和收益数据长度不同
    def alignData(self, returnData, factorData):
        returnDataDf = pd.DataFrame(data=returnData.values, index=returnData.index.get_level_values('secID'), columns=[returnData.name])
        factorDataDf = pd.DataFrame()
        for i in factorData.index.values:
            data = pd.DataFrame(data=factorData[i].values, index=factorData[i].index.get_level_values('secID'), columns=[i])
            factorDataDf = pd.concat([data, factorDataDf], axis=1)
        ret = pd.concat([returnDataDf, factorDataDf], axis=1).dropna()
        return ret

    def calcRankIC(self, layerFactor):
        """
        :param layerFactor: pd.Series, 分层因子
        :return: pd.DataFrame, index = tiaoCangDate, col = [alpha factor names]
        给定分层因子，计算每个调仓日对应的alpha因子IC
        """
        low = pd.DataFrame(index=self.__tiaoCangDate, columns=[self.__alphaFactorNames])
        high = pd.DataFrame(index=self.__tiaoCangDate, columns=[self.__alphaFactorNames])

        for j in range(1, len(self.__tiaoCangDate)):   #对时间做循环，得到每个时间点的rankIC
            date = self.__tiaoCangDate[j]
            prevDate = self.__tiaoCangDate[j-1]
            groupLow, groupHigh = self.getGroup(date, layerFactor)         #分组
            returnLow = self.getReturn(groupLow, date)
            returnHigh = self.getReturn(groupHigh, date)     #得到当期收益序列
            factorLow = self.getAlphaFactor(groupLow, prevDate)
            factorHigh = self.getAlphaFactor(groupHigh, prevDate)      #得到上期因子序列
            tableLow = self.alignData(returnLow, factorLow)
            tableHigh = self.alignData(returnHigh, factorHigh)
            for k in self.__alphaFactorNames:
                tmplow, _ = st.spearmanr(tableLow['RETURN'], tableLow[k])
                tmphigh, _ = st.spearmanr(tableHigh['RETURN'], tableHigh[k])
                low[k][j] = tmplow
                high[k][j] = tmphigh

        return low, high

    def getAnalysis(self, layerFactor):
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
        if percentile>= 85:
            return 9
        elif 50 <= percentile < 85:
            return 9*(percentile/35.0 - 50.0/35.0)**0.7
        elif 15 <= percentile < 50:
            return -9*(percentile/35.0 - 50.0/35.0)**0.7
        else:
            return -9

    def calcAlphaFactorWeightOnDate(self, date):
        """
        :param: date, datetime, tiaoCangDate
        :return:  pd.DataFrame,  index = [layerFactor], cols= [alpha factor name]
        给定调仓日，计算alpha因子的加权矩阵
        """
        tiaoCangDateIndex = self.__tiaoCangDate.index(date) + 1
        pyFinAssert(tiaoCangDateIndex >= self.__tiaoCangDateWindowSize, ValueError, "first weight calc date must be later than moving window last date")

        retLow = pd.DataFrame(columns=[self.__alphaFactorNames])
        retHigh = pd.DataFrame(columns=[self.__alphaFactorNames])

        for layerFactor in self.__layerFactor:
            low, high = self.calcRankIC(layerFactor)
            lowToUse = low.iloc[tiaoCangDateIndex - self.__tiaoCangDateWindowSize:tiaoCangDateIndex]
            highToUse = high.iloc[tiaoCangDateIndex - self.__tiaoCangDateWindowSize:tiaoCangDateIndex]
            weightLow = lowToUse.mean(axis=0) / lowToUse.std(axis=0)
            weightHigh = highToUse.mean(axis=0) / highToUse.std(axis=0)
            retLow = pd.concat([retLow, pd.DataFrame(weightLow, index=layerFactor, columns=[self.__alphaFactorNames])], axis=1)
            retHigh = pd.concat([retHigh, pd.DataFrame(weightHigh, index=layerFactor, columns=[self.__alphaFactorNames])], axis=1)

        return retLow, retHigh

    def calcAlphaFactorRank(self, secIDs, date):
        """
        :param secIDs, list, a group of sec ids
        :param date, datetime, tiaoCangDate
        :return:  pd.DataFrame,  index = secID, cols= [alpha factor name]
        给定调仓日，计算secIDs的alpha因子的排位
        """
        alphaFactor = self.getAlphaFactor(secIDs, date)
        alphaFactorRank = alphaFactor.rank()
        ret = pd.DataFrame(alphaFactorRank, index=secIDs, columns=self.__alphaFactorNames)
        return ret




if __name__ == "__main__":
    factor = FactorLoader('2015-10-05', '2015-12-31', ['CAP', 'ROE','RETURN'])
    factorData = factor.getFactorData()
    analyzer = DCAMAnalyzer([factorData['CAP']],
                            [factorData['ROE']],
                            factorData['RETURN'],
                            factor.getTiaoCangDate(),
                            startDate='2015-10-05',
                            endDate='2015-12-31')
    #print analyzer.getReturn(['603997.SH','603998.SH'],'2015-12-31')
    #print analyzer.getFactor(['603997.SH','603998.SH'],'2015-12-31')




