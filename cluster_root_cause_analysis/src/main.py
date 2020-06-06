from src.cluster import ts_cluster
from src.granger import granger_init, granger_cause
from fastsst import SingularSpectrumTransformation
import matplotlib.pylab as plt
import numpy as np
import csv


class cg_cause(object):
    def __init__(self):
        self.name_list = []
        self.data = []
        self.sst_data = []
        self.normal_cluster = {}
        self.sst_cluster = {}
        self.normal_assignments = {}
        self.sst_assignments = {}
        self.normal_granger = {}
        self.sst_granger = {}
        self.graph = {}
        self.sst_graph = {}
        self.relation_set = {}


    def load_data(self):
        with open('../datasets/all_data.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                self.name_list.append(row[0])

                np_row = np.array(row[1:-1]).astype(np.float)
                if (np_row == 0).all():
                    continue
                self.data.append(np_row)

                sst = SingularSpectrumTransformation(win_length=30)
                score = sst.score_offline(np_row)
                self.sst_data.append(score)
            
            
    def cluster(self):
        normal = ts_cluster(4)
        normal.k_means_clust(self.data, 10, 20, 4)
        # test.sc_score(data)
        normal_centroids = normal.get_centroids()
        self.normal_assignments = normal.get_assignments()
        print("ASS", self.normal_assignments)
        for key, value in normal_centroids.items():
            self.normal_cluster[key] = value.tolist()
        print("CENT", self.normal_cluster)
        # sc_score = test.sc_score()
        for i in normal_centroids.values():
            plt.plot(i)
        plt.show()
        
        
    def cluster_sst(self):
        sst = ts_cluster(4)
        sst.k_means_clust(self.data, 10, 20, 4)
        # test.sc_score(data)
        sst_centroids = sst.get_centroids()
        self.sst_assignments = sst.get_assignments()
        print("ASS", self.sst_assignments)
        for key, value in sst_centroids.items():
            self.sst_cluster[key] = value.tolist()
        print("CENT", self.sst_cluster)
        # sc_score = test.sc_score()
        for i in sst_centroids.values():
            plt.plot(i)
        plt.show()
        
        
    def granger(self):
        self.graph = granger_init(self.normal_cluster)
        self.sst_graph = granger_init(self.sst_cluster)
        print(self.graph)
        print(self.sst_graph)

    def find_relation(self, name):
        series_set = []
        ind = self.name_list.index(name)
        for key, value in self.normal_assignments.items():
            if ind in value:
                series_set = list(set(series_set).union(set(self.normal_assignments[key])))
                if key in self.graph:
                    for item1 in self.graph[key]:
                        series_set = list(set(series_set).union(set(self.normal_assignments[item1])))
                if key in self.sst_graph:
                    for item2 in self.sst_graph[key]:
                        series_set = list(set(series_set).union(set(self.normal_assignments[item2])))
        for kpi in series_set:
            self.relation_set[self.name_list[kpi]] = self.data[kpi]

    def cause(self, name):
        ind = self.name_list.index(name)
        anomaly = []
        anomaly.append(name)
        for item in self.data[ind]:
            anomaly.append(item)
        result = granger_cause(self.relation_set, anomaly)
        sorted_res = sorted(result.items(), key=lambda x: x[1], reverse=True)
        service = {}
        for item in sorted_res:
            print(item)
            for ind, letter in enumerate(item[0]):
                if letter != '/':
                    continue
                else:
                    if item[0][(ind + 1):(ind + 5)] in service:
                        service[item[0][(ind + 1):(ind + 5)]] = service[item[0][(ind + 1):(ind + 5)]] + 1
                    else:
                        service[item[0][(ind + 1):(ind + 5)]] = 1
                    break
        service = sorted(service.items(), key=lambda x: x[1], reverse=True)
        for item in service:
            print(item)
        return service


if __name__ == '__main__':
    test = cg_cause()
    test.load_data()
    test.cluster()
    test.cluster_sst()
    test.granger()
    test.find_relation("service/front-end/qps(2xx)")
    test.cause("service/front-end/qps(2xx)")
