#-*- coding: UTF-8 -*-
from src.alarm_detect import alarm_detect
from src.association import association_analysis
from src.cluster import cluster
from src.sst import use_sst
from dtaidistance import dtw


def kpi_init(kpi_series):
    # time_series_set（时间，指标）对
    # 读取数据
    time_series_set = []
    for row in kpi_series:
        row[0] = int(row[0])
        row[1] = float(row[1])
        time_series_set.append(row)

    return time_series_set


def cluster_control(kpi_series, name):
    time_series_set = kpi_init(kpi_series)
    cluster(time_series_set, name)
    return True


def association_control(kpi_series, events):
    time_series_set = kpi_init(kpi_series)
    result = association_analysis(time_series_set, events)
    return result


def sst_control(kpi_series):
    time_series_set = kpi_init(kpi_series)
    result = use_sst(time_series_set)
    return result


def detect_control(kpi_series, alarm_line):
    time_series_set = kpi_init(kpi_series)
    alarm_series = alarm_detect(time_series_set, alarm_line)
    return alarm_series


def distance_control(kpi_series_normal, kpi_series_abnormal):
    time_series_normal = []
    for row in kpi_series_normal:
        temp = float(row[1])
        time_series_normal.append(temp)
    print(time_series_normal)
    time_series_abnormal = []
    for row in kpi_series_abnormal:
        temp = float(row[1])
        time_series_abnormal.append(temp)
    print(time_series_abnormal)
    distance = dtw.distance(time_series_normal, time_series_abnormal)
    print(distance)
    return distance
