# -*- coding: utf-8 -*-
import datetime
import pandas as pd
from PyFin.DateUtilities import Date
from PyFin.DateUtilities import Calendar
from PyFin.Enums import BizDayConventions
from pyStratLib.utils import dateutils


def getReportDate(actDate, returnBizDay=True):
    """
    :param actDate: str/datetime.datetime, 任意日期
    :return: datetime, 对应应使用的报告日期， 从wind数据库中爬取
    此函数的目的是要找到，任意时刻可使用最新的季报数据的日期，比如2-20日可使用的最新季报是去年的三季报（对应日期为9-30），

    """

    if isinstance(actDate, str):
        actDate = Date.strptime(actDate)
    elif isinstance(actDate, datetime.date):
        actDate = Date.fromDateTime(actDate)
    actMonth = actDate.month()
    actYear = actDate.year()
    if 1 <= actMonth <= 3:  # 第一季度使用去年三季报的数据
        year = actYear - 1
        month = 9
        day = 30
    elif 4 <= actMonth <= 7:  # 第二季度使用当年一季报
        year = actYear
        month = 3
        day = 31
    elif 8 <= actMonth <= 9:  # 第三季度使用当年中报
        year = actYear
        month = 6
        day = 30
    else:
        year = actYear  # 第四季度使用当年三季报
        month = 9
        day = 30
    if returnBizDay:
        dateAdj = Calendar('China.SSE').adjustDate(Date(year, month, day), BizDayConventions.Preceding)
        ret = dateAdj.toDateTime()
    else:
        ret = datetime.datetime(year, month, day)
    return ret

def getUniverseSingleFactor(path, IndexName=['tradeDate', 'secID'], returnBizDay=True):
    """
    :param path: str, path of csv file, col =[datetime, secid, factor]
    :param IndexName: multi index name to be set
    :return: pd.Series, multiindex =[datetime, secid] value = factor
    """

    factor = pd.read_csv(path)
    factor.columns = ['tradeDate', 'secID', 'factor']
    factor['tradeDate'] = pd.to_datetime(factor['tradeDate'], format='%Y%m%d')
    factor = factor.dropna()
    factor = factor[factor['secID'].str.contains(r'^[^<A>]+$$')]  # 去除类似AXXXX的代码(IPO终止)
    if returnBizDay:
        bizDay = dateutils.mapToBizDay(factor['tradeDate'])
    index = pd.MultiIndex.from_arrays([bizDay.values, factor['secID'].values], names=IndexName)
    ret = pd.Series(factor['factor'].values, index=index, name='factor')
    return ret


def adjustFactorDate(factorRaw, startDate, endDate, freq='m'):
    """
    :param factorRaw: pd.DataFrame, multiindex =['tradeDate','secID']
    :param startDate: str/datetime.datetime, start date of factor data
    :param endDate: str/datetime.datetime, end date of factor data
    :param freq: str, optional, tiaocang frequency
    :return: pd.Series, multiindex =[datetime, secid] / pd.DataFrame
    此函数的主要目的是 把原始以报告日为对应日期的因子数据 改成 调仓日为日期（读取对应报告日数据）
    """

    ret = pd.Series()

    # 获取调仓日日期
    tiaoCangDate = dateutils.getPosAdjDate(startDate, endDate, freq=freq)
    reportDate = [getReportDate(date, returnBizDay=True) for date in tiaoCangDate]

    for i in range(len(tiaoCangDate)):
        query = factorRaw.loc[factorRaw.index.get_level_values('tradeDate') == reportDate[i]]
        query = query.reset_index().drop('tradeDate', axis=1)
        query['tiaoCangDate'] = [tiaoCangDate[i]] * query['secID'].count()
        ret = pd.concat([ret, query], axis=0)
    ret = ret[['tiaoCangDate', 'secID', 'factor']]  # 清理列

    index = pd.MultiIndex.from_arrays([ret['tiaoCangDate'].values, ret['secID'].values],
                                      names=['tiaoCangDate', 'secID'])
    ret = pd.Series(ret['factor'].values, index=index, name='factor')

    return ret


def getMultiIndexData(multiIdxData, firstIdxName, firstIdxVal, secIdxName=None, secIdxVal=None):
    """
    :param multiIdxData: pd.Series, multi-index =[firstIdxName, secIdxName]
    :param firstIdxName: str, first index name of multiIndex series
    :param firstIdxVal: str/list/datetime.date, selected value of first index
    :param secIdxName: str, second index name of multiIndex series
    :param secIdxVal: str/list/datetime.date, selected valuer of second index
    :return: pd.Series, selected value with multi-index = [firstIdxName, secIdxName]
    """

    if isinstance(firstIdxVal, basestring) or isinstance(firstIdxVal, datetime.datetime):
        firstIdxVal = [firstIdxVal]

    data = multiIdxData.loc[multiIdxData.index.get_level_values(firstIdxName).isin(firstIdxVal)]
    if secIdxName is not None:
        if isinstance(secIdxVal, basestring) or isinstance(secIdxVal, datetime.date):
            secIdxVal = [secIdxVal]
        data = data.loc[data.index.get_level_values(secIdxName).isin(secIdxVal)]
    return data


if __name__ == "__main__":
    path = '..//..//data//return//monthlyReturn.csv'
    factorRaw = getUniverseSingleFactor(path)
    print adjustFactorDate(factorRaw, '2015-01-05', '2015-12-01')
