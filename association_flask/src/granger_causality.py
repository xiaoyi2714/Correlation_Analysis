# -*- coding: utf-8 -*-

from statsmodels.tsa.stattools import grangercausalitytests
import csv
from sklearn import preprocessing
import numpy as np


def granger_init(kpi_series_first, kpi_series_second):
    time_series_first = []
    for row in kpi_series_first:
        temp = float(row[1])
        time_series_first.append(temp)
    time_series_second = []
    for row in kpi_series_second:
        temp = float(row[1])
        time_series_second.append(temp)
    data = []
    for i in range(min(len(time_series_first), len(time_series_second))):
        data.append([time_series_first[i], time_series_second[i]])
    print(data)
    return data


def granger_test(kpi_series_first, kpi_series_second):
    data = granger_init(kpi_series_first, kpi_series_second)
    std_data = preprocessing.scale(data)
    granger = grangercausalitytests(std_data, maxlag=4)
    print(granger[1][0]['ssr_ftest'][1])
    return granger[1][0]['ssr_ftest'][1]
