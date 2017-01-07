# coding=utf-8
import datetime
from PyFin.DateUtilities import Calendar
from PyFin.DateUtilities import Date
from PyFin.DateUtilities import Period
from PyFin.DateUtilities import Schedule
from PyFin.Enums import BizDayConventions
from PyFin.Enums import TimeUnits
from PyFin.Enums.Weekdays import Weekdays

_freqDict = {'d': TimeUnits.Days,
             'b': TimeUnits.BDays,
             'w': TimeUnits.Weeks,
             'm': TimeUnits.Months,
             'y': TimeUnits.Years}


def changeDateToDatetime(date, format='%Y-%m-%d'):
    datetime.datetime.strptime(str(date), format)


def mapToBizDayList(dateList, calendar='China.SSE', convention=BizDayConventions.Preceding):
    """
    :param dateList: list of dates in datetime types
    :param calendar: str, optional, name of the calendar to use in dates math
    :param convention: str, optional, pyFin date conventions
    :return:
    用更快的方式计算, 避免对每个日期进行循环
    """
    uniqueDateList = list(set(dateList))
    pyDateList = [Date(i.year, i.month, i.day) for i in uniqueDateList]
    pyDateList = [Calendar(calendar).adjustDate(i, BizDayConventions.Preceding) for i in pyDateList]
    bizDayList = [changeDateToDatetime(i.toDateTime()) for i in pyDateList]
    mapDict = dict()
    # TODO finish this function
    ret = []
    return ret



def getPosAdjDate(startDate, endDate, format="%Y-%m-%d", calendar='China.SSE', freq='m'):
    """
    :param startDate: str/datetime.date, start date of strategy
    :param endDate: str/datetime.date, end date of strategy
    :param format: optional, format of the string date
    :param calendar: str, optional, name of the calendar to use in dates math
    :param freq: str, optional, the frequency of data
    :return: list of datetime, pos adjust dates
    """
    if isinstance(startDate, str) and isinstance(endDate, str):
        dStartDate = Date.strptime(startDate, format)
        dEndDate = Date.strptime(endDate, format)
    elif isinstance(startDate, datetime.date) and isinstance(endDate, datetime.date):
        dStartDate = Date.fromDateTime(startDate)
        dEndDate = Date.fromDateTime(endDate)

    cal = Calendar(calendar)
    posAdjustDate = Schedule(dStartDate,
                             dEndDate,
                             Period(1, _freqDict[freq]),
                             cal,
                             BizDayConventions.Unadjusted)
    # it fails if setting dStartDate to be first adjustment date, then use Schedule to compute the others
    # so i first compute dates list in each period, then compute the last date of each period
    # last day of that period(month) is the pos adjustment date
    if _freqDict[freq] == TimeUnits.Weeks:
        PosAdjustDate = [Date.toDateTime(Date.nextWeekday(date, Weekdays.Friday)) for date in posAdjustDate[:-1]]
    elif _freqDict[freq] == TimeUnits.Months:
        PosAdjustDate = [Date.toDateTime(cal.endOfMonth(date)) for date in posAdjustDate[:-1]]
    elif _freqDict[freq] == TimeUnits.Years:
        PosAdjustDate = [Date.toDateTime(Date(date.year(), 12, 31)) for date in posAdjustDate[:-1]]

    # PyFin returns datetime.date type, but datetime.datetime type makes life easier
    PosAdjustDate = [changeDateToDatetime(date) for date in PosAdjustDate]

    return PosAdjustDate


if __name__ == "__main__":
    print getPosAdjDate('2013-5-20', '2016-12-20', freq='y')
    print getPosAdjDate(datetime.datetime(2013, 5, 20), datetime.datetime(2016, 12, 20), freq='y')
