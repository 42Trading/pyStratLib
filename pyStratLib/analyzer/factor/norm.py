# -*- coding: utf-8 -*-
# ref: https://uqer.io/community/share/55ff6ce9f9f06c597265ef04
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

_industryDict = {
    '801190.SI': '金融服务(申万)',
    '801200.SI': '商业贸易(申万)',
    '801210.SI': '休闲服务(申万)',
    '801220.SI': '信息服务(申万)',
    '801230.SI': '综合(申万)',
    '801170.SI': '交通运输(申万)',
    '801160.SI': '公用事业(申万)',
    '801150.SI': '医药生物(申万)',
    '801140.SI': '轻工制造(申万)',
    '801130.SI': '纺织服装(申万)',
    '801120.SI': '食品饮料(申万)',
    '801110.SI': '家用电器(申万)',
    '801100.SI': '信息设备(申万)',
    '801090.SI': '交运设备(申万)',
    '801080.SI': '电子(申万)',
    '801070.SI': '机械设备(申万)',
    '801010.SI': '农林牧渔(申万)',
    '801020.SI': '采掘(申万)',
    '801030.SI': '化工(申万)',
    '801040.SI': '钢铁(申万)',
    '801050.SI': '有色金属(申万)',
    '801060.SI': '建筑建材(申万)',
    '801180.SI': '房地产(申万)',
    '801880.SI': '汽车(申万)',
    '801790.SI': '非银金融(申万)',
    '801780.SI': '银行(申万)',
    '801770.SI': '通信(申万)',
    '801760.SI': '传媒(申万)',
    '801750.SI': '计算机(申万)',
    '801740.SI': '国防军工(申万)',
    '801730.SI': '电气设备(申万)',
    '801720.SI': '建筑装饰(申万)',
    '801710.SI': '建筑材料(申万)',
    '801890.SI': '机械设备(申万)'
}


def winsorize(factor, nb_std_or_quantile=3):
    """
    :param factor: pd.Series, 原始截面因子
    :param nb_std_or_quantile: int or list, optional, 如果是int, 则代表number of std, 如果是list[0.025,0.975] 则使用quantile作为极值判断的标准
    :return: pd.Series, 去极值化后的因子
    """

    factor = factor.copy()
    if isinstance(nb_std_or_quantile, int):
        median = factor.median()
        std = factor.std()
        factor[factor < median - nb_std_or_quantile * std] = median - nb_std_or_quantile * std
        factor[factor > median + nb_std_or_quantile * std] = median + nb_std_or_quantile * std
    elif isinstance(nb_std_or_quantile, list) and len(nb_std_or_quantile) == 2:
        q = factor.quantile(nb_std_or_quantile)
        factor[factor < q.iloc[0]] = q.iloc[0]
        factor[factor > q.iloc[1]] = q.iloc[1]
    else:
        raise ValueError('nb_std_or_quantile should be list or int type')
    return factor


def standardize(factor):
    """
    :param factor: pd.Series, 原始截面因子
    :return: pd.Series, 标准化后的因子  (x - mean)/std

    """
    factor = factor.copy()
    mean = factor.mean()
    std = factor.std()
    ret = factor.apply(lambda x: (x - mean) / std)
    return ret


def getIndustryMatrix(industry, mktCap=None):
    """
    :param industry: pd.Series, index = secID, value = 行业名称
    :param mktCap: pd.Series, index = secID, value = 市值
    :return: numpy.matrix, 行业虚拟矩阵，see alphaNote
    """
    secIDs = industry.index.tolist()
    nbSecId = len(secIDs)
    uniqueIndustry = industry.unique()
    nbUnqiueIndustry = len(uniqueIndustry)
    ret = np.zeros((nbSecId, nbUnqiueIndustry))
    for i in range(len(secIDs)):
        colIndex = np.where(uniqueIndustry == industry[i])[0]
        ret[i][colIndex] = 1.0

    if mktCap is not None:
        arrayCap = mktCap.values.reshape(mktCap.values.shape[0], 1)
        # 合并两个矩阵构成大矩阵
        ret = np.hstack((ret, arrayCap))

    return ret


def neutralize(factor, industry, cap=None):
    """
    :param factor: pd.Series, 原始截面因子
    :param industry: pd.Series, value = 行业名称
    :param cap: optional, pd.Series, value = cap value
    :return: 中性化后的因子
    """
    # 通过concat把数据对齐
    if cap is None:
        data = pd.concat([factor, industry], join='inner', axis=1)
        lcap = None
    else:
        data = pd.concat([factor, industry, cap], join='inner', axis=1)
        lcap = np.log(data[data.columns[2]])

    factor = data[data.columns[0]]
    industry = data[data.columns[1]]

    linreg = LinearRegression(fit_intercept=False)
    Y = factor
    X = getIndustryMatrix(industry, lcap)
    model = linreg.fit(X, Y)
    coef = np.mat(linreg.coef_)
    a = np.dot(X, coef.T)
    residues = Y.values - a.A1
    ret = pd.Series(residues, index=factor.index, name=factor.name).dropna()
    return ret


def normalize(factor, industry=None, cap=None):
    """
    :param factor:  pd.Series, 原始截面因子
    :param industry: pd.Series, value = 行业名称
    :param cap: optional, pd.Series, value = cap value
    :return: 去极值、中性化、标准化的因子
    """
    x = winsorize(factor)
    y = neutralize(x, industry, cap)
    ret = standardize(y)
    return ret


if __name__ == "__main__":
    index = ['000001.SZ', '000002.SZ', '000003.SZ', '000004.SZ', '000005.SZ', '000006.SZ', '000007.SZ', '000008.SZ',
             '000009.SZ', '000010.SZ']
    factor = [10, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
              1.0]
    industry = ['801190.SI', '801190.SI', '801200.SI', '801200.SI', '801200.SI', '801200.SI', '801200.SI', '801200.SI',
                '801200.SI', '801200.SI']
    cap = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    factor = pd.Series(factor, index=index)
    industry = pd.Series(industry, index=['000001.SZ', '000002.SZ', '100003.SZ', '000004.SZ', '000005.SZ', '000006.SZ',
                                          '000007.SZ', '000008.SZ', '000009.SZ', '000010.SZ'])
    cap = pd.Series(cap, index=index)
    print normalize(factor, industry, cap)
