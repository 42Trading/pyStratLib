# -*- coding: utf-8 -*-
# 从wind服务器读取数据的初版，希望完善后能合并入Algo-Trading package中
# http://image.dajiangzhang.com/djz/download/20140928/WindMatlab.pdf
# http://image.dajiangzhang.com/djz/download/20140928/WindAPIFAQ.pdf

from enum import IntEnum
from enum import unique
import pandas as pd
from WindPy import w

@unique
class FreqType(IntEnum):
    MIN5 = 5
    HOUR = 60
    EOD = 0



class WindMarketDataHandler(object):

    def __init__(self, secID, startDate, endDate, freq=None, fields=None):
        self._secID = secID
        self._startDate = startDate
        self._endDate = endDate
        self._freq = FreqType.EOD if freq is None else freq
        self._fields = 'open,high,low,close,volume' if fields is None else fields

    @property
    def dataFreq(self):
        return self._freq

    @dataFreq.setter
    def dataFreq(self, freq):
        self._freq = freq

    @property
    def dataFields(self):
        return self._fields

    @dataFields.setter
    def dataFields(self, fields):
        self._fields = fields

    def getSingleSecIDData(self, secID=None):
        secID = self._secID[0] if secID is None else secID
        ret = pd.DataFrame()
        w.start()
        try:
            # 一次只能一个品种
            if self._freq == FreqType.EOD:
                rawData = w.wsd(secID, self._fields, self._startDate, self._endDate)
            else:
                #TODO starttime and endtime in fact should depend on type of sec, i.e. some sec has night session markets
                startTime = self._startDate + '09:00:00'
                endTime = self._endDate + '15:00:00'
                barSize = 'BarSize=' + str(self._freq)
                rawData = w.wsi(secID, self._fields, startTime, endTime, barSize)

            if rawData is not None:
                 output = {'tradeDate':rawData.Times,
                            'open':rawData.Data[0],
                            'high':rawData.Data[1],
                            'low':rawData.Data[2],
                            'close':rawData.Data[3],
                            'volume':rawData.Data[4]}
                 ret = pd.DataFrame(output)
                 if self._freq == FreqType.EOD:
                     ret['tradeDate'] = ret['tradeDate'].apply(lambda x: x.strftime('%Y-%m-%d'))
                 ret = ret.set_index('tradeDate')
        except ValueError:
            pass

        w.stop()
        return ret

    def getSecIDsData(self):
        """
        :return: pd.DataFrame, multi index = [tradeDate, secID]
        """
        ret = pd.DataFrame()
        for secID in self._secID:
            data = self.getSingleSecIDData(secID)
            tradeDateIndex = data.index.tolist()
            secIDIndex = [secID] * len(data)
            index = pd.MultiIndex.from_arrays([tradeDateIndex, secIDIndex], names=['tradeDate', 'secID'])
            multiIndexData = pd.DataFrame(data.values, index=index)
            ret = pd.concat([ret, multiIndexData], axis=0)
        return ret

if __name__ == "__main__":
    windData = WindMarketDataHandler(secID=['000300.SH', '000001.SZ'],
                                     startDate='2015-01-01',
                                     endDate='2015-02-01')
    print windData.getSecIDsData()