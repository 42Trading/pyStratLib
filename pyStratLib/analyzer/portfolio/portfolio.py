# -*- coding: utf-8 -*-


class Portfolio(object):
    """
    用以处理alpha选股后的净值计算和绘图等问题
    等Algo-Trading package有动态universe功能后,此类便可以退休了
    """
    def __init__(self, secIDs, histPrice, initCash=1000000000.0, weight=None):
        """
        :param secIDs: pd.DataFrame, multi index = [tiaoCangDate, secID] value=[score, industry(optional)]
        :param histPrice: pd.DataFrame, multi index = [tradeDate, secID]
        :param weight: list, optional, weight of secs in ptf
        :return:
        """
        self._secIDs = secIDs
        self._histPrice = histPrice
        self._weight = weight

    def calcEquityCurvesBetweenTiaoCangDate(self, tiaoCangStartDate, tiaoCangEndDate):
        return



