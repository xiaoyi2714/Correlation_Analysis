#-*- coding: UTF-8 -*-

import csv
from dtaidistance import dtw
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from dtaidistance import clustering



def cluster(time_series_set, name):

    path = "./static/cluster_data.csv"
    cluster_data = csv.reader(open(path, 'r'))

    name_list = []
    series_list = []

    for row in cluster_data:
        #print(row)
        #print("row", row)
        name_list.append(row[0])
        #print("name", name_list)
        series = row[1:]
        #print("series", series)
        float_series = []
        for i in series:
            float_series.append(float(i))
        np_series = np.array(float_series)
        temp_series = stats.zscore(np_series)
        series_list.append(temp_series)

    if name not in name_list:
        # timeseries是性能指标序列
        time_series = []
        time_series_with_name = []
        time_series_with_name.append(name)
        for row in time_series_set:
            time_series.append(row[1])
            time_series_with_name.append(row[1])
        #print(time_series)

        with open(path, 'a') as f:
            csv_write = csv.writer(f)
            csv_write.writerow(time_series_with_name)
            f.close()

        name_list.append(name)
        float_series = []
        for i in time_series:
            float_series.append(float(i))
        np_series = np.array(float_series)
        temp_series = stats.zscore(np_series)
        series_list.append(temp_series)


    # Custom Hierarchical clustering
    model1 = clustering.Hierarchical(dtw.distance_matrix_fast, {})
    cluster_idx = model1.fit(series_list)
    # Augment Hierarchical object to keep track of the full tree
    model2 = clustering.HierarchicalTree(model1)
    cluster_idx = model2.fit(series_list)
    # SciPy linkage clustering
    model3 = clustering.LinkageTree(dtw.distance_matrix_fast, {})
    cluster_idx = model3.fit(series_list)

    # model2.plot("hierarchy.png")

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 10))
    show_ts_label = lambda idx: name_list[idx]
    model2.plot("hierarchy.png", axes=ax, show_ts_label=show_ts_label,
               show_tr_label=True, ts_label_margin=-10,
               ts_left_margin=10, ts_sample_length=1)
