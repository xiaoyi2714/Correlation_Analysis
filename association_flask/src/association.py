#-*- coding: UTF-8 -*-
from association_analysis import alarm_association


def association_analysis(kpi_series, events):

    OFFSET = 16

    # 建立时间序列
    # timeseries是性能指标序列
    time_series = []
    for row in kpi_series:
        time_series.append(row[1])
        
    # time是性能指标对应的全时间序列
    time = []
    for row in kpi_series:
        time.append(row[0])

    # 事件时间戳错误
    for key in events.keys():
        for item in events[key]:
            if item not in time:
                return "error"

    rel_set = {}
    for key in events.keys():
        event_series_set = []
        iter_event = 0
        event = events[key][1:]
        event.sort()
        for item in event:
            while item != time[iter_event]:
                iter_event += 1
            row = []
            for j in range(OFFSET + 0, OFFSET + 10):
                row.append(time_series[iter_event + j])
            event_series_set.append(row)
            iter_event += 1

        relativity_avg = 0
        for iter_score in range(10):
            relativity = alarm_association.feature_screen(event, event_series_set, time_series)
            # print(i, relativity)
            relativity_avg = relativity_avg + relativity
        relativity = relativity_avg / 10
        rel_set[key] = relativity
        result = {}
        for k in sorted(rel_set, key=rel_set.__getitem__, reverse=True):
            result[k] = rel_set[k]

    return result
    # event_series_set = []
    # i = 0
    # for item in events:
    #     while item != time[i]:
    #         i += 1
    #     row = []
    #     for j in range(OFFSET + 0, OFFSET + 10):
    #         row.append(time_series[i + j])
    #     event_series_set.append(row)
    #     i += 1
    #
    # relativity_avg = 0
    # for i in range(10):
    #     relativity = alarm_association.feature_screen(events, event_series_set, time_series)
    #     # print(i, relativity)
    #     relativity_avg = relativity_avg + relativity
    # relativity = relativity_avg / 10
    # return relativity
