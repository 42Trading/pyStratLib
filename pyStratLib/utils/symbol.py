# -*- coding: utf-8 -*-
from PyFin.Utilities import pyFinAssert

def windConvert2DataYes(windSecID):
    """
    :param windCode: list wind sec id, i.e. 000300.SH/000300.sh
    :return: datayes type code, 1.e. 000300.xshg
    """

    pyFinAssert(isinstance(windSecID, list), "windSecID must be in list type")
    windSecIDList = windSecID
    windSecIDList = [s.lower() for s in windSecIDList]

    ret = []
    for s in windSecIDList:
        secIDComp = s.split('.')
        if secIDComp[1] == 'sh':
            dataYesID = secIDComp[0] + '.xshg'
        elif secIDComp[1] == 'sz':
            dataYesID = secIDComp[0] + '.xshe'
        else:
            raise ValueError("Unknown securitie name {0}. Security names without"
                                 " exchange suffix is not allowed".format(s))
        ret.append(dataYesID)

    return ret

def DataYesConvert2Wind(DataYesID):
    """
    :param DataYesID: list, datayes type code, 1.e. 000300.xshg
    :return: list, wind sec id, i.e. 000300.SH/000300.sh
    """
    #TODO how to deal with index id?

    pyFinAssert(isinstance(DataYesID, list), "windSecID must be in list type")
    DataYesIDList = DataYesID
    DataYesIDList = [s.lower() for s in DataYesIDList]

    ret = []
    for s in DataYesIDList:
        secIDComp = s.split('.')
        if secIDComp[1] == 'xshg':
            windSecID = secIDComp[0] + '.sh'
        elif secIDComp[1] == 'xshe':
            windSecID = secIDComp[0] + '.sz'
        else:
            raise ValueError("Unknown securitie name {0}. Security names without"
                                 " exchange suffix is not allowed".format(s))
        ret.append(windSecID)

    return ret


if __name__ == "__main__":
    print windConvert2DataYes(['000300.SH'])