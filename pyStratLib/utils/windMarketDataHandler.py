# -*- coding: utf-8 -*-
# 从wind服务器读取数据的初版，希望完善后能合并入Algo-Trading package中
# http://image.dajiangzhang.com/djz/download/20140928/WindMatlab.pdf
# http://image.dajiangzhang.com/djz/download/20140928/WindAPIFAQ.pdf

from enum import IntEnum
from enum import unique
import pandas as pd
from WindPy import w
from PyFin.Utilities import pyFinAssert
from pyStratLib.enums.dfReturn import dfReturnType

@unique
class FreqType(IntEnum):
    MIN5 = 5
    HOUR = 60
    EOD = 0



class WindMarketDataHandler(object):

    def __init__(self, secID, startDate, endDate, freq=None, fields=None, returnType=dfReturnType.DateIndexAndSecIDCol):
        self._secID = secID
        self._startDate = startDate
        self._endDate = endDate
        self._freq = FreqType.EOD if freq is None else freq
        self._fields = ['open', 'high', 'low', 'close', 'volume'] if fields is None else fields
        self._returnType = returnType

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

    @property
    def returnFormat(self):
        return self._returnType

    @returnFormat.setter
    def dataFreq(self, returnType):
        self._returnType = returnType

    def getSingleSecData(self, secID=None):
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
                output = {'tradeDate':rawData.Times}
                for field in self._fields:
                    output[field] = rawData.Data[self._fields.index(field)]
                ret = pd.DataFrame(output)
                if self._freq == FreqType.EOD:
                    ret['tradeDate'] = ret['tradeDate'].apply(lambda x: x.strftime('%Y-%m-%d'))
                ret = ret.set_index('tradeDate')
        except ValueError:
            pass

        w.stop()
        return ret

    def getSecPriceData(self):
        """
        :return: pd.DataFrame, index=[tradeDate], cols = sec id
        this return format is to be consistent with alphalens package
        """
        ret = pd.DataFrame()
        if self._returnType == dfReturnType.DateIndexAndSecIDCol:
            pyFinAssert(len(self._fields) == 1,
                        'each sec id must query only 1 fields of data while in fact {f} fields is queried'.format(len(self._fields)))
            for secID in self._secID:
                data = self.getSingleSecData(secID)
                ret = pd.concat([ret, data], axis=1)
            ret.columns = self._secID
        else:
            raise NotImplementedError

        return ret

if __name__ == "__main__":
    windData = WindMarketDataHandler(secID=['000300.SH', '000001.SZ'],
                                     startDate='2015-01-01',
                                     endDate='2015-02-01',
                                     fields='close')
    print windData.getSecPriceData()