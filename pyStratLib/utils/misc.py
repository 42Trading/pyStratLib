
import pandas as pd
from PyFin.Utilities import pyFinAssert




def top(df, column=None, n=5):
    """
    :param df: pd.DataFrame/Series
    :param column: str, col name to be sorted
    :param n: int, optional, top n element to be returned
    :return: pd.Series, larget n element in col
    """
    if isinstance(df, pd.Series):
        ret = df.sort_values(ascending=False)[:n]
    else:
        pyFinAssert(column is not None, "Specify the col name or use pandas Series type of data")
        ret = df.sort_values(by=column, ascending=False)[:n]

    return ret