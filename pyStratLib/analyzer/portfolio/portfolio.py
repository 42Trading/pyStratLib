# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pyStratLib.analyzer.factor.cleanData import getMultiIndexData

class Portfolio(object):
    """
    用以处理alpha选股后的净值计算和绘图等问题
    等Algo-Trading package有动态universe功能后,此类便可以退休了
    """
    def __init__(self, secSelected, histPrice, initCash=1000000000.0, weight=None):
        """
        :param secIDs: pd.DataFrame, multi index = [tiaoCangDate, secID] value=[score(optional), industry(optional)]
        :param histPrice: pd.DataFrame, multi index = [tradeDate, secID]
        :param weight: list, optional, weight of secs in ptf
        :return:
        """
        self._secSelected = secSelected
        self._histPrice = histPrice
        self._initCash = initCash
        self._weight = weight
        self._tiaoCangDate = self._secSelected.index.get_level_values('tiaoCangDate').tolist()

    def _getSecPriceOnDate(self, data, date, dateColName='tradeDate', priceColName='close', resetIndexColName='secID'):
        price = getMultiIndexData(data, dateColName, date, priceColName)
        price = price.reset_index().set_index(resetIndexColName)
        price = price[priceColName]
        price.columns = [date]
        return price


    def _calcPtfValueBetweenTiaoCangDate(self, initPtfValue, tiaoCangStartDate, tiaoCangEndDate):
        ptfSecID = getMultiIndexData(self._secSelected, 'tiaoCangDate', tiaoCangStartDate)

        # get sec id list at tiaoCangDate
        secIDlist = ptfSecID.index.get_level_values('secID').tolist()
        nbSecID = len(secIDlist)
        ptfValue = pd.DataFrame(index=secIDlist)

        # get price date table between tiaoCangDate
        priceData = self._histPrice.loc[self._histPrice.index.get_level_values('tradeDate')<= tiaoCangEndDate]
        priceData = priceData.loc[priceData.index.get_level_values('tradeDate') >= tiaoCangStartDate]

        # get price table at tiaoCangDate
        price = self._getSecPriceOnDate(priceData, tiaoCangStartDate)

        # concat price with sec id selected
        # TODO: handle the nan case
        ptfValue = pd.concat([ptfValue, price], join_axes=[ptfValue.index], axis=1)

        # get quantity list at tiaoCangDate
        if self._weight is None:
            # equal weight
            ptfValue['quantity'] = self._initCash / nbSecID / ptfValue[tiaoCangStartDate]

        # loop over all trade dates to calc ptf value
        tradeDateList = priceData.index.get_level_values('tradeDate').tolist()
        ret = pd.Series(index=tradeDateList)
        ret.loc[tradeDateList[0]] = initPtfValue
        for date in tradeDateList[1:]:
            price = self._getSecPriceOnDate(priceData, date)
            ptfValue = pd.concat([ptfValue, price], join_axes=[ptfValue.index], axis=1)
            ret.loc[date] = np.sum(ptfValue['quantitiy'] * ptfValue[date])

        return ret


    def calcPtfValueCurve(self):
        ret = pd.Series()

        for i in range(len(self._tiaoCangDate)-1):
            tiaoCangStartDate = self._tiaoCangDate[i]
            tiaoCangEndDate = self._tiaoCangDate[i+1]
            initPtfValue = self._initCash if i == 0 else ret.iloc[-1]
            ptfCurve = self._calcPtfValueBetweenTiaoCangDate(initPtfValue, tiaoCangStartDate, tiaoCangEndDate)
            ret = pd.concat([ret, ptfCurve], axis=0)

        return ret


