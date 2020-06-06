#-*- coding: UTF-8 -*-
import numpy as np
import banpei
import csv


#计算平均数
def average_num(num):
    nsum = 0.0
    for i in range(len(num)):
        nsum += float(num[i])
    return nsum / len(num)


def t_test(front, rear):
    u_front = average_num(front)
    u_rear = average_num(rear)
    front_float = np.array(front).astype(np.float)
    std_dev_front = np.std(front_float)
    rear_float = np.array(rear).astype(np.float)
    std_dev_rear = np.std(rear_float)
    t_score = (u_rear - u_front) / ((((std_dev_front ** 2) + (std_dev_rear ** 2)) / len(front)) ** 0.5)
    return t_score


def use_sst(time_series):
    #
    # OFFSET = 0
    # WIN = 2
    # model = banpei.SST(w=10)
    #
    # # #timeseries是性能指标序列
    # # time_series = []
    # # for row in time_series_set:
    # #     time_series.append(row[1])
    # # # time是性能指标对应的全时间序列
    # # time = []
    # # for row in time_series_set:
    # #     time.append(row[0])
    # # print("time", time_series)
    # score = model.detect(time_series)
    # #print(score)
    # lst = score.tolist()
    #
    # #print("score", lst)
    #
    # iter = len(lst) - 1
    # while iter > (OFFSET - 1):
    #     lst[iter] = lst[iter - OFFSET]
    #     iter -= 1
    # for k in range(0, 32):
    #     lst[k] = 0.0
    #
    #
    #
    #
    # # 用t-score给sst结果判断正负
    # # for i in range(2, (len(lst) - 2)):
    # #     front = time_series[(i - WIN): i: 1]
    # #     rear = time_series[i: (i + WIN): 1]
    # #     t_score = t_test(front, rear)
    # #     if t_score < 0:
    # #         lst[i] = -lst[i]
    #
    #
    #
    # # 极值
    # # x = np.array(lst)
    # # avgLst = average_num(lst)
    # # npMaxList = argrelextrema(x, np.greater)[0]
    # # maxlst = npMaxList.tolist()
    # # maxList = []
    # # for max in maxlst:
    # #     if lst[max] > avgLst*5:
    # #         maxList.append(max)
    # # print(maxList)
    # # tScoreSeries = []
    # # for item in maxList:
    # #     print(time[item])
    # #     front = time_series[(item - WIN):item:1]
    # #     rear = time_series[item:(item + WIN):1]
    # #     t_score = t_test(front, rear, WIN)
    # #     tScoreSeries.append([item, t_score])
    # # print(tScoreSeries)
    # #
    # # temp = tScoreSeries[0]
    # # tempFront = 0
    # # tempRear = 0
    # # for item in tScoreSeries[1:]:
    # #     if temp[-1] * item[-1] < 0:
    # #         if (temp[-1] > 0) and (item[-1] < 0):
    # #             continue
    # #         else:
    # #             if (temp[-1] < 0) and (item[-1] > 0):
    # #                 tempRear = (temp[0] + item[0]) / 2
    # #                 for i in range(tempFront, tempRear):
    # #                     sst_list[i][-1] = - sst_list[i][-1]
    # #                 tempFront = tempRear
    # #                 temp = item
    # #     else:
    # #         continue
    # #
    # # lstSeries = []
    # # for item in sst_list:
    # #     lstSeries.append(item[-1])
    # # print(lstSeries)
    #
    # # sst_list = []
    # # for i in range(len(time)):
    # #     row = [time[i], lst[i]]
    # #     sst_list.append(row)

    model = banpei.SST(w=50)
    results = model.detect(time_series)

    return results


def sst_init():
    with open('../dataset/all_data.csv', 'r') as kpi:
        with open('../dataset/sst_test.csv', 'w') as sst:
            reader = csv.reader(kpi)
            writer = csv.writer(sst)
            file = []
            for row in reader:
                file.append(row)
            for row in file:
                sst = use_sst(row[1:])
            #     plt.plot(sst)
            #
            # plt.show()
                writer.writerow([row[0]] + sst)


if __name__ == '__main__':
    sst_init()