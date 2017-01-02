#coding=utf-8

from numpy import sort
from numpy import mean
from numpy import cov
from numpy.linalg import eig
from numpy import mat
from numpy import argsort
from PyFin.Utilities import pyFinAssert

def eigValPct(eigVals, pct):
    """
    :param eigVals: np.array/list, 所有特征值组成的向量
    :param pct: 阈值
    :return: 给定百分比阈值,返回需要降低到多少维度
    """
    pyFinAssert(0.0 <= pct <= 1.0, ValueError, "pct ({0:f}) must be between 0.0 and 1.0".format(pct))
    sortEigVals = sort(eigVals)
    sortEigVals = sortEigVals[-1::-1] # 特征值从大到小排列
    eigValsSum = sum(sortEigVals)
    tempSum = 0
    num = 0
    for i in sortEigVals:
        tempSum += i
        num += 1
        if tempSum >= eigValsSum * pct:
            return num

    return len(sortEigVals)


def pcaDecomp(dataMat, pct=0.9):
    """
    :param dataMat: np.maths, 数据矩阵, 列向量为特征向量
    :param pct: 阈值, 降维后需要达到的方差占比
    :return: 降维后的数据集, 和 重构数据
    """

    meanVals = mean(dataMat, axis=0) # 对每一列求均值
    meanRemoved = dataMat - meanVals
    covMat = cov(meanRemoved, rowvar=0)
    eigVals, eigVects = eig(mat(covMat))
    k = eigValPct(eigVals, pct)
    eigValInd = argsort(eigVals)
    eigValInd = eigValInd[:-(k+1):-1]
    redEigVects = eigVects[:, eigValInd] #返回排序后特征值对应的特征向量redEigVects（主成分）
    lowDDataMat = meanRemoved * redEigVects #将原始数据投影到主成分上得到新的低维数据lowDDataMat
    reconMat = lowDDataMat * redEigVects.T + meanVals #得到重构数据reconMat
    return lowDDataMat, reconMat



if __name__ == "__main__":
    eigValPct([1,2,3], 0.9)




