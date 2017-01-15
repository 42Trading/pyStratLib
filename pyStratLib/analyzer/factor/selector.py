# -*- coding: utf-8 -*-

import pandas as pd
from pyStratLib.analyzer.benchmark.benchmark import Benchmark
from pyStratLib.analyzer.factor.cleanData import getMultiIndexData


def secSelectorOnDate(  secScore,
                        date,
                        nbSecSelected=100,
                        benchmark=None,
                        saveFile=False):
    """
    :param secScore: pd.DataFrame, index=secID, col=[score, industry(optional)]
    :param date: std, datetime.datetime
    :param nbSecSelected: int, 总共需要选出的股票数量
    :param benchmark: Benchmark class type, optional, 比较基准
    :param saveFile: bool, optional, 是否把股票筛选结果保存为本地文件
    :return: pd.Series, sec id selected
    """
    secID = []
    secScore.sort_values(ascending=False, inplace=True)
    # 判断是否选股时是否需要做到行业中性
    if benchmark is not None:
        indsutryNbSecSelected = benchmark.calcNbSecSelectedOnDate(date, nbSecSelected)
        for name, group in secScore.groupby(level='industry'):
            nbSec = indsutryNbSecSelected[name]
            topSec = group[:nbSec+1]
            secID += topSec.index.get_level_values('secID')
    else:
        secID = secScore.index.tolist()[:nbSecSelected+1]

    ret = pd.Series(secID, name=date)

    return ret
