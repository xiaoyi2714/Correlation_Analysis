from statsmodels.tsa.stattools import grangercausalitytests
from sklearn import preprocessing
import numpy as np
from graphviz import Digraph


def granger_test(series):
    std_data = preprocessing.scale(series)
    granger = grangercausalitytests(std_data, maxlag=4)
    return granger[1][0]['ssr_ftest'][1]


def granger_cause(relation_set, anomaly):
    res_set = {}
    for k1, v1 in relation_set.items():
        if k1 == anomaly[0]:
            continue
        pair = []
        v2 = anomaly[1:-1]
        for ind in range(min(len(v1), len(v2))):
            pair.append([v1[ind], v2[ind]])
        print("PAIR", pair)
        temp = float(granger_test(pair))
        if temp <= 0.1:
            res_set[k1] = temp
    print(res_set)
    return res_set


def granger_init(data):
    length = len(data)
    granger_res = np.ones((length, length))
    for k1, v1 in data.items():
        for k2, v2 in data.items():
            if k1 == k2:
                continue
            pair = []
            for ind in range(min(len(v1), len(v2))):
                pair.append([v1[ind], v2[ind]])
            print(pair)
            granger_res[k2][k1] = float(granger_test(pair))
    print(granger_res)

    graph = {}
    for k1, v1 in data.items():
        for k2, v2 in data.items():
            if granger_res[k1][k2] <= 0.1:
                if k2 in graph:
                    graph[k2].append(k1)
                else:
                    graph[k2] = [k1]

    g = Digraph('granger')
    for k1, v1 in data.items():
        g.node(label=str(k1), name=str(k1), color='black')
    for k1, v1 in data.items():
        for k2, v2 in data.items():
            if granger_res[k1][k2] <= 0.1:
                g.edge(str(k1), str(k2), color='red')
    g.view()

    return graph
