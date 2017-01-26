# -*- coding: utf-8 -*-

from pyStratLib.analyzer.factor.loadData import getMultiIndexData

class Benchmark(object):
    def __init__(self, industryWeight):
        self.__industryWeight = industryWeight

    def getIndustryWeightOnDate(self, date):
        return getMultiIndexData(self.__industryWeight, 'tiaoCangDate', date)

    def getIndustryWeightOnName(self, industryName):
        if not industryName.endwith('SI'):
            industryName = _industryDict.keys()[_industryDict.values().index(industryName)]
        return getMultiIndexData(self.__industryWeight, 'secID', industryName)

    def calcNbSecSelectedOnDate(self, date, nbSecSelected=100):
        """
        :param date:
        :param nbSecSelected:
        :return: dict, key = industry, value = nb sec to be selected
        """
        industryWeightOnDate = self.getIndustryWeightOnDate(date)
        nbSecSelectedByIndustry = industryWeightOnDate * nbSecSelected/100.0
        nbSecSelectedByIndustry  = nbSecSelectedByIndustry.astype(int)
        nbSecSelectedByIndustry = nbSecSelectedByIndustry.reset_index().set_index('secID')
        ret = nbSecSelectedByIndustry[industryWeightOnDate.name].to_dict()
        return ret

    @classmethod
    def mapIndustryCodeToName(cls, industry):
        """
        :param industry: pd.Series, index = secID, value = industry code
        :return: pd.Series, index = secID, value = industry name
        """
        industry = industry.copy()
        ret = industry.apply(lambda x: _industryDict[x])
        ret.name = industry.name
        return ret



_industryDict = {
    '801190.SI': '金融服务',
    '801200.SI': '商业贸易',
    '801210.SI': '休闲服务',
    '801220.SI': '信息服务',
    '801230.SI': '综合',
    '801170.SI': '交通运输',
    '801160.SI': '公用事业',
    '801150.SI': '医药生物',
    '801140.SI': '轻工制造',
    '801130.SI': '纺织服装',
    '801120.SI': '食品饮料',
    '801110.SI': '家用电器',
    '801100.SI': '信息设备',
    '801090.SI': '交运设备',
    '801080.SI': '电子',
    '801070.SI': '机械设备',
    '801010.SI': '农林牧渔',
    '801020.SI': '采掘',
    '801030.SI': '化工',
    '801040.SI': '钢铁',
    '801050.SI': '有色金属',
    '801060.SI': '建筑建材',
    '801180.SI': '房地产',
    '801880.SI': '汽车',
    '801790.SI': '非银金融',
    '801780.SI': '银行',
    '801770.SI': '通信',
    '801760.SI': '传媒',
    '801750.SI': '计算机',
    '801740.SI': '国防军工',
    '801730.SI': '电气设备',
    '801720.SI': '建筑装饰',
    '801710.SI': '建筑材料',
    '801890.SI': '机械设备'
}

