#-*- coding: UTF-8 -*-

import csv
from association_analysis import alarm_association

#if __name__=='__main__':
def association_analysis(event, alldata):

    for row in event:
        alarmtime = row[1:]
    alarmtime.sort()
    for i in range(len(alarmtime)):
        alarmtime[i] = int(alarmtime[i])

    timeseries_set = []

    next(alldata)
    for row in alldata:
        row[0] = int(row[0])
        row[1] = float(row[1])
        timeseries_set.append(row)

    event = []
    i = 0
    for time in alarmtime:
        while time != timeseries_set[i][0]:
            i += 1
        row = []
        for j in range(0,5):
            row.append(timeseries_set[i + j][1])
        event.append(row)
        i += 1

    timeseries = []
    for row in timeseries_set:
        timeseries.append(row[1])

    # 生成混合集
    mixset, alarm_number, random_number = alarm_association.mixdata(alarmtime, event, timeseries)

    flag = alarm_association.feature_screen(mixset, alarm_number, random_number)
    print(flag)

    return flag
