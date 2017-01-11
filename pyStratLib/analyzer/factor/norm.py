# -*- coding: utf-8 -*-
# ref: https://uqer.io/community/share/55ff6ce9f9f06c597265ef04
import pandas as pd
import numpy as np
from PyFin.Utilities import pyFinAssert
from sklearn.linear_model import LinearRegression




_industryDict = {
#TODO fill out the dict

}

def winsorize(factors, nb_std_or_quantile=3):
    """
    :param factors: pd.Series, 原始截面因子
    :param nb_std_or_quantile: int or list, optional, 如果是int, 则代表number of std, 如果是list[0.025,0.975] 则使用quantile作为极值判断的标准
    :return: pd.Series, 去极值化后的因子
    """

    factors = factors.copy()
    if isinstance(nb_std_or_quantile,int):
        mean = factors.mean()
        std = factors.std()
        factors[factors<mean - nb_std_or_quantile*std] = mean - nb_std_or_quantile*std
        factors[factors>mean + nb_std_or_quantile*std] = mean + nb_std_or_quantile*std
    elif isinstance(nb_std_or_quantile,list) and len(nb_std_or_quantile)==2:
        q = factors.quantile(nb_std_or_quantile)
        factors[factors<q.iloc[0]] = q.iloc[0]
        factors[factors>q.iloc[1]] = q.iloc[1]
    else:
        raise ValueError('nb_std_or_quantile should be list or int type')
    return factors


def standardize(factors):
    """
    :param factors: pd.Series, 原始截面因子
    :return: pd.Series, 标准化后的因子  (x - mean)/std

    """
    factors = factors.copy()
    mean = factors.mean()
    std = factors.std()
    ret = factors.apply(lambda x: (x - mean)/std)
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
        arrayCap = mktCap.values.reshape(mktCap.values.shape[0],1)
        # 合并两个矩阵构成大矩阵
        ret = np.hstack((ret, arrayCap))

    return ret


def neutralize(factors, industry, cap=None):
    """
    :param factors: pd.Series, 原始截面因子
    :param industry: pd.Series, value = 行业名称
    :param cap: optional, pd.Series, value = cap value
    :return: 中性化后的因子
    """
    pyFinAssert(factors.size == industry.size, ValueError,
                "factor size {0} does not equal to industry size {1}".format(factors.size, industry.size))
    linreg = LinearRegression(fit_intercept=False)
    Y = factors
    if cap is None:
        X = getIndustryMatrix(industry)
    else:
        pyFinAssert(industry.size == cap.size, ValueError,
                "industry size {0} does not equal to cap size {1}".format(industry.size, cap.size))
        lcap = np.log(cap)
        X = getIndustryMatrix(industry, lcap)

    model = linreg.fit(X, Y)
    coef = np.mat(linreg.coef_)
    a = np.dot(X, coef.T)
    residues = Y.values - a.A1
    ret = pd.Series(residues, index=factors.index)
    return ret


if __name__ == "__main__":
    factors = pd.Series([5.0,5.0,3.0,10.0], index=['000001.SZ','000002.SZ','000003.SZ','000004.SZ'])
    cap = pd.Series([50.0,100.0,20.0, 20.0], index=['000001.SZ','000002.SZ','000003.SZ','000004.SZ'])
    industry = pd.Series(['801190.SI', '801190.SI','801200.SI','801200.SI'], index=['000001.SZ','000002.SZ','000003.SZ','000003.SZ'])
    print neutralize(factors, industry, cap)
