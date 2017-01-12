# -*- coding: utf-8 -*-

from enum import IntEnum
from enum import unique

@unique
class FactorNormType(IntEnum):
    Null = 0
    IndustryNeutral = 1
    IndustryAndCapNeutral = 2