# -*- coding: utf-8 -*-
import datetime
import unittest

from pyStratLib.utils.dateutils import getPosAdjDate


class TestDateUtils(unittest.TestCase):
    def testGetPosAdjDate(self):
        calculated = getPosAdjDate('2015-06-01', '2016-06-01', format="%Y-%m-%d", calendar='China.SSE', freq='m')
        expected = [datetime.datetime(2015, 6, 30), datetime.datetime(2015, 7, 31), datetime.datetime(2015, 8, 31),
                    datetime.datetime(2015, 9, 30), datetime.datetime(2015, 10, 30), datetime.datetime(2015, 11, 30),
                    datetime.datetime(2015, 12, 31), datetime.datetime(2016, 1, 29), datetime.datetime(2016, 2, 29),
                    datetime.datetime(2016, 3, 31), datetime.datetime(2016, 4, 29), datetime.datetime(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate(datetime.datetime(2015, 6, 1), datetime.datetime(2016, 6, 1), format="%Y-%m-%d",
                                   calendar='China.SSE', freq='m')
        expected = [datetime.datetime(2015, 6, 30), datetime.datetime(2015, 7, 31), datetime.datetime(2015, 8, 31),
                    datetime.datetime(2015, 9, 30), datetime.datetime(2015, 10, 30), datetime.datetime(2015, 11, 30),
                    datetime.datetime(2015, 12, 31), datetime.datetime(2016, 1, 29), datetime.datetime(2016, 2, 29),
                    datetime.datetime(2016, 3, 31), datetime.datetime(2016, 4, 29), datetime.datetime(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015/06/01', '2016/06/01', format="%Y/%m/%d", calendar='China.SSE', freq='m')
        expected = [datetime.datetime(2015, 6, 30), datetime.datetime(2015, 7, 31), datetime.datetime(2015, 8, 31),
                    datetime.datetime(2015, 9, 30), datetime.datetime(2015, 10, 30), datetime.datetime(2015, 11, 30),
                    datetime.datetime(2015, 12, 31), datetime.datetime(2016, 1, 29), datetime.datetime(2016, 2, 29),
                    datetime.datetime(2016, 3, 31), datetime.datetime(2016, 4, 29), datetime.datetime(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate(datetime.datetime(2015, 6, 1), datetime.datetime(2016, 6, 1), format="%Y/%m/%d",
                                   calendar='China.SSE', freq='m')
        expected = [datetime.datetime(2015, 6, 30), datetime.datetime(2015, 7, 31), datetime.datetime(2015, 8, 31),
                    datetime.datetime(2015, 9, 30), datetime.datetime(2015, 10, 30), datetime.datetime(2015, 11, 30),
                    datetime.datetime(2015, 12, 31), datetime.datetime(2016, 1, 29), datetime.datetime(2016, 2, 29),
                    datetime.datetime(2016, 3, 31), datetime.datetime(2016, 4, 29), datetime.datetime(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015-06-01', '2016-06-01')
        expected = [datetime.datetime(2015, 6, 30), datetime.datetime(2015, 7, 31), datetime.datetime(2015, 8, 31),
                    datetime.datetime(2015, 9, 30), datetime.datetime(2015, 10, 30), datetime.datetime(2015, 11, 30),
                    datetime.datetime(2015, 12, 31), datetime.datetime(2016, 1, 29), datetime.datetime(2016, 2, 29),
                    datetime.datetime(2016, 3, 31), datetime.datetime(2016, 4, 29), datetime.datetime(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate(datetime.datetime(2015, 6, 1), datetime.datetime(2016, 6, 1))
        expected = [datetime.datetime(2015, 6, 30), datetime.datetime(2015, 7, 31), datetime.datetime(2015, 8, 31),
                    datetime.datetime(2015, 9, 30), datetime.datetime(2015, 10, 30), datetime.datetime(2015, 11, 30),
                    datetime.datetime(2015, 12, 31), datetime.datetime(2016, 1, 29), datetime.datetime(2016, 2, 29),
                    datetime.datetime(2016, 3, 31), datetime.datetime(2016, 4, 29), datetime.datetime(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015-06-01', '2016-06-01', format="%Y-%m-%d", calendar='China.SSE', freq='w')
        expected = [datetime.datetime(2015, 6, 5), datetime.datetime(2015, 6, 12), datetime.datetime(2015, 6, 19),
                    datetime.datetime(2015, 6, 26), datetime.datetime(2015, 7, 3), datetime.datetime(2015, 7, 10),
                    datetime.datetime(2015, 7, 17), datetime.datetime(2015, 7, 24), datetime.datetime(2015, 7, 31),
                    datetime.datetime(2015, 8, 7), datetime.datetime(2015, 8, 14), datetime.datetime(2015, 8, 21),
                    datetime.datetime(2015, 8, 28), datetime.datetime(2015, 9, 4), datetime.datetime(2015, 9, 11),
                    datetime.datetime(2015, 9, 18), datetime.datetime(2015, 9, 25), datetime.datetime(2015, 10, 2),
                    datetime.datetime(2015, 10, 9), datetime.datetime(2015, 10, 16), datetime.datetime(2015, 10, 23),
                    datetime.datetime(2015, 10, 30), datetime.datetime(2015, 11, 6), datetime.datetime(2015, 11, 13),
                    datetime.datetime(2015, 11, 20), datetime.datetime(2015, 11, 27), datetime.datetime(2015, 12, 4),
                    datetime.datetime(2015, 12, 11), datetime.datetime(2015, 12, 18), datetime.datetime(2015, 12, 25),
                    datetime.datetime(2016, 1, 1), datetime.datetime(2016, 1, 8), datetime.datetime(2016, 1, 15),
                    datetime.datetime(2016, 1, 22), datetime.datetime(2016, 1, 29), datetime.datetime(2016, 2, 5),
                    datetime.datetime(2016, 2, 12), datetime.datetime(2016, 2, 19), datetime.datetime(2016, 2, 26),
                    datetime.datetime(2016, 3, 4), datetime.datetime(2016, 3, 11), datetime.datetime(2016, 3, 18),
                    datetime.datetime(2016, 3, 25), datetime.datetime(2016, 4, 1), datetime.datetime(2016, 4, 8),
                    datetime.datetime(2016, 4, 15), datetime.datetime(2016, 4, 22), datetime.datetime(2016, 4, 29),
                    datetime.datetime(2016, 5, 6), datetime.datetime(2016, 5, 13), datetime.datetime(2016, 5, 20),
                    datetime.datetime(2016, 5, 27)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate(datetime.datetime(2015, 6, 1), datetime.datetime(2016, 6, 1), format="%Y-%m-%d",
                                   calendar='China.SSE', freq='w')
        expected = [datetime.datetime(2015, 6, 5), datetime.datetime(2015, 6, 12), datetime.datetime(2015, 6, 19),
                    datetime.datetime(2015, 6, 26), datetime.datetime(2015, 7, 3), datetime.datetime(2015, 7, 10),
                    datetime.datetime(2015, 7, 17), datetime.datetime(2015, 7, 24), datetime.datetime(2015, 7, 31),
                    datetime.datetime(2015, 8, 7), datetime.datetime(2015, 8, 14), datetime.datetime(2015, 8, 21),
                    datetime.datetime(2015, 8, 28), datetime.datetime(2015, 9, 4), datetime.datetime(2015, 9, 11),
                    datetime.datetime(2015, 9, 18), datetime.datetime(2015, 9, 25), datetime.datetime(2015, 10, 2),
                    datetime.datetime(2015, 10, 9), datetime.datetime(2015, 10, 16), datetime.datetime(2015, 10, 23),
                    datetime.datetime(2015, 10, 30), datetime.datetime(2015, 11, 6), datetime.datetime(2015, 11, 13),
                    datetime.datetime(2015, 11, 20), datetime.datetime(2015, 11, 27), datetime.datetime(2015, 12, 4),
                    datetime.datetime(2015, 12, 11), datetime.datetime(2015, 12, 18), datetime.datetime(2015, 12, 25),
                    datetime.datetime(2016, 1, 1), datetime.datetime(2016, 1, 8), datetime.datetime(2016, 1, 15),
                    datetime.datetime(2016, 1, 22), datetime.datetime(2016, 1, 29), datetime.datetime(2016, 2, 5),
                    datetime.datetime(2016, 2, 12), datetime.datetime(2016, 2, 19), datetime.datetime(2016, 2, 26),
                    datetime.datetime(2016, 3, 4), datetime.datetime(2016, 3, 11), datetime.datetime(2016, 3, 18),
                    datetime.datetime(2016, 3, 25), datetime.datetime(2016, 4, 1), datetime.datetime(2016, 4, 8),
                    datetime.datetime(2016, 4, 15), datetime.datetime(2016, 4, 22), datetime.datetime(2016, 4, 29),
                    datetime.datetime(2016, 5, 6), datetime.datetime(2016, 5, 13), datetime.datetime(2016, 5, 20),
                    datetime.datetime(2016, 5, 27)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015/06/01', '2016/06/01', format="%Y/%m/%d", calendar='China.SSE', freq='y')
        expected = [datetime.datetime(2015, 12, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate(datetime.datetime(2015, 6, 1), datetime.datetime(2016, 6, 1), format="%Y/%m/%d",
                                   calendar='China.SSE', freq='y')
        expected = [datetime.datetime(2015, 12, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015-06-01', '2016-06-01', format="%Y-%m-%d", calendar='China.IB', freq='m')
        expected = [datetime.datetime(2015, 6, 30), datetime.datetime(2015, 7, 31), datetime.datetime(2015, 8, 31),
                    datetime.datetime(2015, 9, 30), datetime.datetime(2015, 10, 30), datetime.datetime(2015, 11, 30),
                    datetime.datetime(2015, 12, 31),
                    datetime.datetime(2016, 1, 29), datetime.datetime(2016, 2, 29), datetime.datetime(2016, 3, 31),
                    datetime.datetime(2016, 4, 29), datetime.datetime(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate(datetime.datetime(2015, 6, 1), datetime.datetime(2016, 6, 1), format="%Y-%m-%d",
                                   calendar='China.IB', freq='m')
        expected = [datetime.datetime(2015, 6, 30), datetime.datetime(2015, 7, 31), datetime.datetime(2015, 8, 31),
                    datetime.datetime(2015, 9, 30), datetime.datetime(2015, 10, 30), datetime.datetime(2015, 11, 30),
                    datetime.datetime(2015, 12, 31),
                    datetime.datetime(2016, 1, 29), datetime.datetime(2016, 2, 29), datetime.datetime(2016, 3, 31),
                    datetime.datetime(2016, 4, 29), datetime.datetime(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015-06-01', '2016-06-01', format="%Y-%m-%d", calendar='Target', freq='m')
        expected = [datetime.datetime(2015, 6, 30), datetime.datetime(2015, 7, 31), datetime.datetime(2015, 8, 31),
                    datetime.datetime(2015, 9, 30), datetime.datetime(2015, 10, 30), datetime.datetime(2015, 11, 30),
                    datetime.datetime(2015, 12, 31),
                    datetime.datetime(2016, 1, 29), datetime.datetime(2016, 2, 29), datetime.datetime(2016, 3, 31),
                    datetime.datetime(2016, 4, 29), datetime.datetime(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate(datetime.datetime(2015, 6, 1), datetime.datetime(2016, 6, 1), format="%Y-%m-%d",
                                   calendar='Target', freq='m')
        expected = [datetime.datetime(2015, 6, 30), datetime.datetime(2015, 7, 31), datetime.datetime(2015, 8, 31),
                    datetime.datetime(2015, 9, 30), datetime.datetime(2015, 10, 30), datetime.datetime(2015, 11, 30),
                    datetime.datetime(2015, 12, 31),
                    datetime.datetime(2016, 1, 29), datetime.datetime(2016, 2, 29), datetime.datetime(2016, 3, 31),
                    datetime.datetime(2016, 4, 29), datetime.datetime(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015-06-01', '2016-06-01', format="%Y-%m-%d", calendar='Null', freq='m')
        expected = [datetime.datetime(2015, 6, 30), datetime.datetime(2015, 7, 31), datetime.datetime(2015, 8, 31),
                    datetime.datetime(2015, 9, 30), datetime.datetime(2015, 10, 31), datetime.datetime(2015, 11, 30),
                    datetime.datetime(2015, 12, 31),
                    datetime.datetime(2016, 1, 31), datetime.datetime(2016, 2, 29), datetime.datetime(2016, 3, 31),
                    datetime.datetime(2016, 4, 30), datetime.datetime(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate(datetime.datetime(2015, 6, 1), datetime.datetime(2016, 6, 1), format="%Y-%m-%d",
                                   calendar='Null', freq='m')
        expected = [datetime.datetime(2015, 6, 30), datetime.datetime(2015, 7, 31), datetime.datetime(2015, 8, 31),
                    datetime.datetime(2015, 9, 30), datetime.datetime(2015, 10, 31), datetime.datetime(2015, 11, 30),
                    datetime.datetime(2015, 12, 31),
                    datetime.datetime(2016, 1, 31), datetime.datetime(2016, 2, 29), datetime.datetime(2016, 3, 31),
                    datetime.datetime(2016, 4, 30), datetime.datetime(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015-06-01', '2016-06-01', format="%Y-%m-%d", calendar='NullCalendar', freq='m')
        expected = [datetime.datetime(2015, 6, 30), datetime.datetime(2015, 7, 31), datetime.datetime(2015, 8, 31),
                    datetime.datetime(2015, 9, 30), datetime.datetime(2015, 10, 31), datetime.datetime(2015, 11, 30),
                    datetime.datetime(2015, 12, 31),
                    datetime.datetime(2016, 1, 31), datetime.datetime(2016, 2, 29), datetime.datetime(2016, 3, 31),
                    datetime.datetime(2016, 4, 30), datetime.datetime(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate(datetime.datetime(2015, 6, 1), datetime.datetime(2016, 6, 1), format="%Y-%m-%d",
                                   calendar='NullCalendar', freq='m')
        expected = [datetime.datetime(2015, 6, 30), datetime.datetime(2015, 7, 31), datetime.datetime(2015, 8, 31),
                    datetime.datetime(2015, 9, 30), datetime.datetime(2015, 10, 31), datetime.datetime(2015, 11, 30),
                    datetime.datetime(2015, 12, 31),
                    datetime.datetime(2016, 1, 31), datetime.datetime(2016, 2, 29), datetime.datetime(2016, 3, 31),
                    datetime.datetime(2016, 4, 30), datetime.datetime(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")
