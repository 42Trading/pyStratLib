# coding=utf-8
import datetime as dt
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


def getPosAdjDate(startDate, endDate, format="%Y-%m-%d", calendar='China.SSE', freq='m'):
    """
    :param startDate: str, start date of strategy
    :param endDate: str, end date of strategy
    :param format: optional, format of the string date
    :param calendar: str, optional, name of the calendar to use in dates math
    :param freq: str, optional, the frequency of data
    :return: list of str, pos adjust dates
    """

    dStartDate = Date.strptime(startDate, format)
    dEndDate = Date.strptime(endDate, format)

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
        strPosAdjustDate = [str(Date.nextWeekday(date, Weekdays.Friday)) for date in posAdjustDate[:-1]]
    elif _freqDict[freq] == TimeUnits.Months:
        strPosAdjustDate = [str(cal.endOfMonth(date)) for date in posAdjustDate[:-1]]
    elif _freqDict[freq] == TimeUnits.Years:
        strPosAdjustDate = [str(Date(date.year(), 12, 31)) for date in posAdjustDate[:-1]]

    return strPosAdjustDate


if __name__ == "__main__":
    print getPosAdjDate('2013-5-20', '2016-12-20', freq='y')
