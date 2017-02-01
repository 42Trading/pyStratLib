# -*- coding: utf-8 -*-

from enum import IntEnum
from enum import unique

@unique
class dfReturnType(IntEnum):
    Null = 0
    MultiIndex = 1
    DateIndexAndSecIDCol = 2