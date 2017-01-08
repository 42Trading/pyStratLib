# -*- coding: utf-8 -*-
import datetime
import unittest

from pyStratLib.utils.dateutils import getPosAdjDate


class TestDateUtils(unittest.TestCase):
    def testGetPosAdjDate(self):
        calculated = getPosAdjDate('2015-06-01', '2016-06-01', format="%Y-%m-%d", calendar='China.SSE', freq='m')
        expected = [datetime.date(2015, 6, 30), datetime.date(2015, 7, 31), datetime.date(2015, 8, 31),
                    datetime.date(2015, 9, 30), datetime.date(2015, 10, 30), datetime.date(2015, 11, 30),
                    datetime.date(2015, 12, 31), datetime.date(2016, 1, 29), datetime.date(2016, 2, 29),
                    datetime.date(2016, 3, 31), datetime.date(2016, 4, 29), datetime.date(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate(datetime.date(2015, 6, 1), datetime.date(2016, 6, 1), format="%Y-%m-%d",
                                   calendar='China.SSE', freq='m')
        expected = [datetime.date(2015, 6, 30), datetime.date(2015, 7, 31), datetime.date(2015, 8, 31),
                    datetime.date(2015, 9, 30), datetime.date(2015, 10, 30), datetime.date(2015, 11, 30),
                    datetime.date(2015, 12, 31), datetime.date(2016, 1, 29), datetime.date(2016, 2, 29),
                    datetime.date(2016, 3, 31), datetime.date(2016, 4, 29), datetime.date(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015/06/01', '2016/06/01', format="%Y/%m/%d", calendar='China.SSE', freq='m')
        expected = [datetime.date(2015, 6, 30), datetime.date(2015, 7, 31), datetime.date(2015, 8, 31),
                    datetime.date(2015, 9, 30), datetime.date(2015, 10, 30), datetime.date(2015, 11, 30),
                    datetime.date(2015, 12, 31), datetime.date(2016, 1, 29), datetime.date(2016, 2, 29),
                    datetime.date(2016, 3, 31), datetime.date(2016, 4, 29), datetime.date(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate(datetime.date(2015, 6, 1), datetime.date(2016, 6, 1), format="%Y/%m/%d",
                                   calendar='China.SSE', freq='m')
        expected = [datetime.date(2015, 6, 30), datetime.date(2015, 7, 31), datetime.date(2015, 8, 31),
                    datetime.date(2015, 9, 30), datetime.date(2015, 10, 30), datetime.date(2015, 11, 30),
                    datetime.date(2015, 12, 31), datetime.date(2016, 1, 29), datetime.date(2016, 2, 29),
                    datetime.date(2016, 3, 31), datetime.date(2016, 4, 29), datetime.date(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015-06-01', '2016-06-01')
        expected = [datetime.date(2015, 6, 30), datetime.date(2015, 7, 31), datetime.date(2015, 8, 31),
                    datetime.date(2015, 9, 30), datetime.date(2015, 10, 30), datetime.date(2015, 11, 30),
                    datetime.date(2015, 12, 31), datetime.date(2016, 1, 29), datetime.date(2016, 2, 29),
                    datetime.date(2016, 3, 31), datetime.date(2016, 4, 29), datetime.date(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate(datetime.date(2015, 6, 1), datetime.date(2016, 6, 1))
        expected = [datetime.date(2015, 6, 30), datetime.date(2015, 7, 31), datetime.date(2015, 8, 31),
                    datetime.date(2015, 9, 30), datetime.date(2015, 10, 30), datetime.date(2015, 11, 30),
                    datetime.date(2015, 12, 31), datetime.date(2016, 1, 29), datetime.date(2016, 2, 29),
                    datetime.date(2016, 3, 31), datetime.date(2016, 4, 29), datetime.date(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015-06-01', '2016-06-01', format="%Y-%m-%d", calendar='China.SSE', freq='w')
        expected = [datetime.date(2015, 6, 5), datetime.date(2015, 6, 12), datetime.date(2015, 6, 19),
                    datetime.date(2015, 6, 26), datetime.date(2015, 7, 3), datetime.date(2015, 7, 10),
                    datetime.date(2015, 7, 17), datetime.date(2015, 7, 24), datetime.date(2015, 7, 31),
                    datetime.date(2015, 8, 7), datetime.date(2015, 8, 14), datetime.date(2015, 8, 21),
                    datetime.date(2015, 8, 28), datetime.date(2015, 9, 4), datetime.date(2015, 9, 11),
                    datetime.date(2015, 9, 18), datetime.date(2015, 9, 25), datetime.date(2015, 10, 2),
                    datetime.date(2015, 10, 9), datetime.date(2015, 10, 16), datetime.date(2015, 10, 23),
                    datetime.date(2015, 10, 30), datetime.date(2015, 11, 6), datetime.date(2015, 11, 13),
                    datetime.date(2015, 11, 20), datetime.date(2015, 11, 27), datetime.date(2015, 12, 4),
                    datetime.date(2015, 12, 11), datetime.date(2015, 12, 18), datetime.date(2015, 12, 25),
                    datetime.date(2016, 1, 1), datetime.date(2016, 1, 8), datetime.date(2016, 1, 15),
                    datetime.date(2016, 1, 22), datetime.date(2016, 1, 29), datetime.date(2016, 2, 5),
                    datetime.date(2016, 2, 12), datetime.date(2016, 2, 19), datetime.date(2016, 2, 26),
                    datetime.date(2016, 3, 4), datetime.date(2016, 3, 11), datetime.date(2016, 3, 18),
                    datetime.date(2016, 3, 25), datetime.date(2016, 4, 1), datetime.date(2016, 4, 8),
                    datetime.date(2016, 4, 15), datetime.date(2016, 4, 22), datetime.date(2016, 4, 29),
                    datetime.date(2016, 5, 6), datetime.date(2016, 5, 13), datetime.date(2016, 5, 20),
                    datetime.date(2016, 5, 27), datetime.date(2016, 6, 3)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate(datetime.date(2015, 6, 1), datetime.date(2016, 6, 1), format="%Y-%m-%d",
                                   calendar='China.SSE', freq='w')
        expected = [datetime.date(2015, 6, 5), datetime.date(2015, 6, 12), datetime.date(2015, 6, 19),
                    datetime.date(2015, 6, 26), datetime.date(2015, 7, 3), datetime.date(2015, 7, 10),
                    datetime.date(2015, 7, 17), datetime.date(2015, 7, 24), datetime.date(2015, 7, 31),
                    datetime.date(2015, 8, 7), datetime.date(2015, 8, 14), datetime.date(2015, 8, 21),
                    datetime.date(2015, 8, 28), datetime.date(2015, 9, 4), datetime.date(2015, 9, 11),
                    datetime.date(2015, 9, 18), datetime.date(2015, 9, 25), datetime.date(2015, 10, 2),
                    datetime.date(2015, 10, 9), datetime.date(2015, 10, 16), datetime.date(2015, 10, 23),
                    datetime.date(2015, 10, 30), datetime.date(2015, 11, 6), datetime.date(2015, 11, 13),
                    datetime.date(2015, 11, 20), datetime.date(2015, 11, 27), datetime.date(2015, 12, 4),
                    datetime.date(2015, 12, 11), datetime.date(2015, 12, 18), datetime.date(2015, 12, 25),
                    datetime.date(2016, 1, 1), datetime.date(2016, 1, 8), datetime.date(2016, 1, 15),
                    datetime.date(2016, 1, 22), datetime.date(2016, 1, 29), datetime.date(2016, 2, 5),
                    datetime.date(2016, 2, 12), datetime.date(2016, 2, 19), datetime.date(2016, 2, 26),
                    datetime.date(2016, 3, 4), datetime.date(2016, 3, 11), datetime.date(2016, 3, 18),
                    datetime.date(2016, 3, 25), datetime.date(2016, 4, 1), datetime.date(2016, 4, 8),
                    datetime.date(2016, 4, 15), datetime.date(2016, 4, 22), datetime.date(2016, 4, 29),
                    datetime.date(2016, 5, 6), datetime.date(2016, 5, 13), datetime.date(2016, 5, 20),
                    datetime.date(2016, 5, 27), datetime.date(2016, 6, 3)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015/06/01', '2016/06/01', format="%Y/%m/%d", calendar='China.SSE', freq='y')
        expected = [datetime.date(2015, 12, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate(datetime.date(2015, 6, 1), datetime.date(2016, 6, 1), format="%Y/%m/%d",
                                   calendar='China.SSE', freq='y')
        expected = [datetime.date(2015, 12, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015-06-01', '2016-06-01', format="%Y-%m-%d", calendar='China.IB', freq='m')
        expected = [datetime.date(2015, 6, 30), datetime.date(2015, 7, 31), datetime.date(2015, 8, 31),
                    datetime.date(2015, 9, 30), datetime.date(2015, 10, 30), datetime.date(2015, 11, 30),
                    datetime.date(2015, 12, 31),
                    datetime.date(2016, 1, 29), datetime.date(2016, 2, 29), datetime.date(2016, 3, 31),
                    datetime.date(2016, 4, 29), datetime.date(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate(datetime.date(2015, 6, 1), datetime.date(2016, 6, 1), format="%Y-%m-%d",
                                   calendar='China.IB', freq='m')
        expected = [datetime.date(2015, 6, 30), datetime.date(2015, 7, 31), datetime.date(2015, 8, 31),
                    datetime.date(2015, 9, 30), datetime.date(2015, 10, 30), datetime.date(2015, 11, 30),
                    datetime.date(2015, 12, 31),
                    datetime.date(2016, 1, 29), datetime.date(2016, 2, 29), datetime.date(2016, 3, 31),
                    datetime.date(2016, 4, 29), datetime.date(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015-06-01', '2016-06-01', format="%Y-%m-%d", calendar='Target', freq='m')
        expected = [datetime.date(2015, 6, 30), datetime.date(2015, 7, 31), datetime.date(2015, 8, 31),
                    datetime.date(2015, 9, 30), datetime.date(2015, 10, 30), datetime.date(2015, 11, 30),
                    datetime.date(2015, 12, 31),
                    datetime.date(2016, 1, 29), datetime.date(2016, 2, 29), datetime.date(2016, 3, 31),
                    datetime.date(2016, 4, 29), datetime.date(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate(datetime.date(2015, 6, 1), datetime.date(2016, 6, 1), format="%Y-%m-%d",
                                   calendar='Target', freq='m')
        expected = [datetime.date(2015, 6, 30), datetime.date(2015, 7, 31), datetime.date(2015, 8, 31),
                    datetime.date(2015, 9, 30), datetime.date(2015, 10, 30), datetime.date(2015, 11, 30),
                    datetime.date(2015, 12, 31),
                    datetime.date(2016, 1, 29), datetime.date(2016, 2, 29), datetime.date(2016, 3, 31),
                    datetime.date(2016, 4, 29), datetime.date(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015-06-01', '2016-06-01', format="%Y-%m-%d", calendar='Null', freq='m')
        expected = [datetime.date(2015, 6, 30), datetime.date(2015, 7, 31), datetime.date(2015, 8, 31),
                    datetime.date(2015, 9, 30), datetime.date(2015, 10, 31), datetime.date(2015, 11, 30),
                    datetime.date(2015, 12, 31),
                    datetime.date(2016, 1, 31), datetime.date(2016, 2, 29), datetime.date(2016, 3, 31),
                    datetime.date(2016, 4, 30), datetime.date(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate(datetime.date(2015, 6, 1), datetime.date(2016, 6, 1), format="%Y-%m-%d",
                                   calendar='Null', freq='m')
        expected = [datetime.date(2015, 6, 30), datetime.date(2015, 7, 31), datetime.date(2015, 8, 31),
                    datetime.date(2015, 9, 30), datetime.date(2015, 10, 31), datetime.date(2015, 11, 30),
                    datetime.date(2015, 12, 31),
                    datetime.date(2016, 1, 31), datetime.date(2016, 2, 29), datetime.date(2016, 3, 31),
                    datetime.date(2016, 4, 30), datetime.date(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate('2015-06-01', '2016-06-01', format="%Y-%m-%d", calendar='NullCalendar', freq='m')
        expected = [datetime.date(2015, 6, 30), datetime.date(2015, 7, 31), datetime.date(2015, 8, 31),
                    datetime.date(2015, 9, 30), datetime.date(2015, 10, 31), datetime.date(2015, 11, 30),
                    datetime.date(2015, 12, 31),
                    datetime.date(2016, 1, 31), datetime.date(2016, 2, 29), datetime.date(2016, 3, 31),
                    datetime.date(2016, 4, 30), datetime.date(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")

        calculated = getPosAdjDate(datetime.date(2015, 6, 1), datetime.date(2016, 6, 1), format="%Y-%m-%d",
                                   calendar='NullCalendar', freq='m')
        expected = [datetime.date(2015, 6, 30), datetime.date(2015, 7, 31), datetime.date(2015, 8, 31),
                    datetime.date(2015, 9, 30), datetime.date(2015, 10, 31), datetime.date(2015, 11, 30),
                    datetime.date(2015, 12, 31),
                    datetime.date(2016, 1, 31), datetime.date(2016, 2, 29), datetime.date(2016, 3, 31),
                    datetime.date(2016, 4, 30), datetime.date(2016, 5, 31)]
        self.assertListEqual(calculated, expected, "Calculated Position Adjustment Date is wrong")
