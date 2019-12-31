#-*- coding: UTF-8 -*-

def alarm_detect(time_series_set, alarm_line):
    STEP = 600

    alarm_data = []
    temp_alarm = 0
    for item in time_series_set:
        if item[-1] > alarm_line:
            if (item[0] - temp_alarm > STEP):
                alarm_data.append(item)
            temp_alarm = item[0]

    # 建立时间序列
    # timeseries是性能指标序列
    time_series = []
    for row in time_series_set:
        time_series.append(row[1])
    # 求序列均值
    avg = average_num(time_series)

    # 找异常范围
    range_series = []
    for item in alarm_data:
        start = item[0]
        end = item[0]
        while (sum(get_series(end, time_series_set)) > avg * 10):
            if (end + STEP) <= time_series_set[-1][0]:
                end = end + STEP
            else:
                break
        while (sum(get_series(start, time_series_set)) > avg * 10):
            if (start - STEP) >= time_series_set[0][0]:
                start = start - STEP
            else:
                break
        range_series.append([start, end + STEP])

    # alarmSeriesSet = []
    # for item in range_series:
    #     i = 0
    #     while item[0] != time_series_set[i][0]:
    #         i += 1
    #     row = []
    #     for j in range(int((item[1] - item[0]) / 60)):
    #         row.append(time_series_set[i + j][-1])
    #     alarmSeriesSet.append(row)

    return range_series;


def get_series(time, time_series):
    series = []
    i = 0
    while time != time_series[i][0]:
        i += 1
    for j in range(10):
        series.append(time_series[i + j])
    return series


#计算平均数
def average_num(num):
    nsum = 0
    for i in range(len(num)):
        nsum += num[i]
    return nsum / len(num)

def sum(data):
    sum = 0
    for i in range(len(data)):
        sum += data[i][-1]
    return sum