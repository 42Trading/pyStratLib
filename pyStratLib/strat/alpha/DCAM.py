# -*- coding: utf-8 -*-
import pandas as pd
import datetime as dt
from pyStratLib.analyzer.factor.dynamicContext import DCAMAnalyzer
from PyFin.api import CLOSE
from AlgoTrading.api import strategyRunner
from AlgoTrading.api import Strategy
from AlgoTrading.api import DataSource
from AlgoTrading.api import PortfolioType




class DCAMStrat(Strategy):

    def __init__(self, path):
        df = pd.read_csv(path)
        self.signals = df
        self.date_index = self.signals.index
        self.close = CLOSE()


    def handle_data(self):
        current_time = self.current_datetime



def run_strat():
    startDate = dt.datetime(2006,10,5)
    endDate = dt.datetime(2016,10,5)

    strategyRunner(userStrategy=DCAMStrat,
                   symbolList=universe,
                   initialCapital=500000,
                   startDate=startDate,
                   endDate=endDate,
                   dataSource=DataSource.WindMarketDataHanlder,
                   freq=min,
                   saveFile=True,
                   plot=True,
                   porfolioType=PortfolioType.CashManageable,
                   logLevel='info')






