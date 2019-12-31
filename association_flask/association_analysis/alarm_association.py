#-*- coding: UTF-8 -*-

from __future__ import division

import copy
import random
import math
from operator import itemgetter


def mixdata(alarmtime, timeseries_set, timeseries):
    """
    :param alarmtime: 报警的时刻序列,已经排好顺序
    :param timeseries_set: 每个报警时刻的时间序列构成的时序集
    :param timeseries: 报警时刻整体区间内的时序数据
    :return:mixset是混合集，alarm_number报警样本个数，random_number随机样本个数
    """
    mixset = []
    alarm_number = 0
    random_number = 0
    randomnum = 20
    timeseries_set_copy = copy.deepcopy(timeseries_set)
    for i in range(len(alarmtime)):
        data = timeseries_set_copy[i]
        data.append('alarm')
        if len(data) > 1 and data not in mixset:
            mixset.append(data)
            alarm_number += 1
    while randomnum > 0:
        end = random.randint(10, len(timeseries))
        start = end - 10
        data = timeseries[start:end]
        data.append("random")
        randomnum -= 1
        if len(data) > 1 and data not in mixset:
            mixset.append(data)
            random_number += 1
    # print("mix", mixset)
    # print(alarm_number)
    # print(random_number)
    return mixset, alarm_number, random_number


def distance(data):
    dis = 0.0
    for i in range(0, len(data) - 1):
        dis += data[i]
    return dis

def feature_screen(event, event_series, timeseries):
    """
    :param mixset: 报警序列与随机序列的混合集
    :param alarm_number: 报警序列个数
    :param random_number: 随机序列个数
    :return: 监控项与报警是否相关
    """
    mixset, alarm_number, random_number = mixdata(event, event_series, timeseries)

    if alarm_number == 0 or random_number == 0:
        return False
    sum_number = alarm_number + random_number
    # #均值
    # mean = (alarm_number/sum_number) ** 2 + (random_number/sum_number) ** 2
    # print("mean", mean)
    # #标准差
    # stdDev = (alarm_number/sum_number) * (random_number/sum_number) * (1 + 4 * (random_number/sum_number) * (alarm_number / sum_number))
    # print("stdDev", stdDev)
    R = 10
    trp = 0
    tempdic = {}
    # print("len", len(mixset))
    for j in range(len(mixset)):
        dis = distance(mixset[j])
        tempdic.setdefault(j, dis)
    temp_list = sorted(tempdic.items(), key = lambda kv:(kv[1], kv[0]))
    # print("len", len(temp_list))

    # print("list", temp_list)
    for k in range(len(temp_list)):
        if (k == 0 or k == len(temp_list) - 1):
            if k == 0:
                nearest = 1
            else:
                nearest = len(temp_list) - 2
        else:
            if (temp_list[k][-1] - temp_list[k - 1][-1]) <= (temp_list[k + 1][-1] - temp_list[k][-1]):
                nearest = k - 1
            else:
                nearest = k + 1
        if mixset[temp_list[k][0]][-1] == mixset[temp_list[nearest][0]][-1]:
            trp += 1
    trp = float(trp / sum_number)
    #print("sum", sum_number)
    #print("trp", trp)
    # check = (abs(trp-mean) / stdDev) * math.sqrt(R*sum_number)
    #print("check", check)
    #print("---------------------------")
    return trp


def get_GR(alarmseries,nomalseries):
    '''
    :param alarmseries: 单一报警的时间序列
    :param nomalseries: 整体报警的时间序列
    :return:
    '''
    cutnum = 10  # 切分份数
    maxvalue = float("-inf")
    minvalue = float("inf")
    GR = 0
    while None in alarmseries:
        alarmseries.remove(None)
    C1 = len(alarmseries)
    if max(alarmseries) > maxvalue:
        maxvalue = max(alarmseries)
    if min(alarmseries) < minvalue:
        minvalue = min(alarmseries)
    while None in nomalseries:
        nomalseries.remove(None)
    C2 = len(nomalseries)
    if max(nomalseries) > maxvalue:
        maxvalue = max(nomalseries)
    if min(nomalseries) < minvalue:
        minvalue = min(nomalseries)
    value_gap = (maxvalue-minvalue) / cutnum
    print(C1)
    print(C2)
    if C1 == 0 or C2 == 0 or value_gap == 0:
        return GR
    HD = (C1 / (C1+C2)) * math.log((C1 / (C1+C2)), 2) + (C2 / (C1+C2)) * math.log((C2 / (C1+C2)), 2)
    Neg = [0] * (cutnum+1)
    Pos = [0] * (cutnum+1)
    for value in alarmseries:
        temp_count = int((value-minvalue) / value_gap) + 1
        if temp_count > cutnum:
            temp_count = cutnum
        Neg[temp_count] += 1
    for value in nomalseries:
        temp_count = int((value-minvalue) / value_gap) + 1
        if temp_count > cutnum:
            temp_count = cutnum
        Pos[temp_count] += 1
    HDA = 0
    HAD = 0
    for j in range(1, cutnum + 1):
        temp = 0
        if Neg[j] != 0 and Pos[j] != 0:
            HAD += ((Neg[j]+Pos[j]) / (C1+C2)) * math.log(((Neg[j]+Pos[j]) / (C1+C2)), 2)
            temp = (Neg[j] / (Neg[j]+Pos[j])) * math.log((Neg[j] / (Neg[j]+Pos[j])), 2) + (Pos[j] / (Neg[j]+Pos[j])) * math.log((Pos[j] / (Neg[j]+Pos[j])), 2)
        elif Neg[j] == 0 and Pos[j] != 0:
            HAD += ((Neg[j]+Pos[j]) / (C1+C2)) * math.log(((Neg[j]+Pos[j]) / (C1 + C2)), 2)
        elif Pos[j] == 0 and Neg[j] != 0:
            HAD += ((Neg[j]+Pos[j]) / (C1+C2)) * math.log(((Neg[j]+Pos[j]) / (C1+C2)), 2)
        HDA += ((Neg[j]+Pos[j]) / (C1+C2)) * temp
    GR = (HD - HDA) / HAD
    return GR