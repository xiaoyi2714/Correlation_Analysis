import matplotlib.pylab as plt
import numpy as np
from statsmodels.tsa.stattools import grangercausalitytests
import random
import csv


class ts_cluster(object):
    def __init__(self, num_clust):
        '''
        num_clust is the number of clusters for the k-means algorithm
        assignments holds the assignments of data points (indices) to clusters
        centroids holds the centroids of the clusters
        '''
        self.num_clust = num_clust
        self.assignments = {}
        self.centroids = {}

    def k_means_clust(self, data, num_iter, w, progress=False):
        '''
        k-means clustering algorithm for time series data.  dynamic time warping Euclidean distance
         used as default similarity measure.
        '''
        cent_random = random.sample(list(data), self.num_clust)
        for c_ind, cent in enumerate(cent_random):
            self.centroids[c_ind] = cent

        for n in range(num_iter):
            if progress:
                print('iteration ' + str(n + 1))
            # assign data points to clusters
            self.assignments = {}
            for ind, i in enumerate(data):
                min_dist = float('inf')
                closest_clust = None
                for c_ind, j in self.centroids.items():
                    if not len(j):
                        continue
                    if self.merge_dis(i, j, w) < min_dist:
                        cur_dist = self.merge_dis(i, j, w)
                        if cur_dist < min_dist:
                            min_dist = cur_dist
                            closest_clust = c_ind
                    # if self.LB_Keogh(i, j, 5) < min_dist:
                    #     cur_dist = self.DTWDistance(i, j, w)
                    #     if cur_dist < min_dist:
                    #         min_dist = cur_dist
                    #         closest_clust = c_ind
                if closest_clust in self.assignments:
                    self.assignments[closest_clust].append(ind)
                else:
                    self.assignments[closest_clust] = [ind]

            # recalculate centroids of clusters
            print(self.assignments)
            centroids_new = self.centroids.copy()
            for key in self.assignments:
                if self.assignments[key]:
                    clust_sum = 0
                    for k in self.assignments[key]:
                        clust_sum = clust_sum + data[k]
                    centroids_new[key] = np.asarray([m / len(self.assignments[key]) for m in clust_sum])
                else:
                    centroids_new[key] = np.asarray([])

            # stop loop
            flag = 1
            for i in centroids_new.keys():
                if not len(centroids_new[i]):
                    continue
                if not (centroids_new[i] == self.centroids[i]).all():
                    flag = 0
            if flag:
                break
            else:
                self.centroids = centroids_new

    def get_centroids(self):
        return self.centroids

    def get_assignments(self):
        return self.assignments

    def plot_centroids(self):
        for i in self.centroids:
            plt.plot(i)
        plt.show()

    def merge_dis(self, a_list, b_list, w):
        cur_dist_0 = self.DTWDistance(a_list, b_list, w)
        # cur_dist_1 = self.granger_dis(a_list, b_list)
        # if np.isnan(cur_dist_1):
        #     cur_dist_1 = 1
        # cur_dist_2 = self.granger_dis(b_list, a_list)
        # if np.isnan(cur_dist_2):
        #     cur_dist_2 = 1
        # # with open('result_1.csv', 'a') as new_file:
        # #     writer = csv.writer(new_file)
        # #     writer.writerow([cur_dist_0, cur_dist_1])
        # cur_dist = ((1 - ((cur_dist_1 + cur_dist_2) / 2)) * 20) + cur_dist_0
        return cur_dist_0

    def granger_dis(self, a_list, b_list):
        data = []
        for iter in range(1, min(len(a_list), len(b_list))):
            a = float(a_list[iter])
            b = float(b_list[iter])
            data.append([a, b])
        granger = grangercausalitytests(data, maxlag=4)
        cur_dist = float(granger[1][0]['ssr_ftest'][1])
        return cur_dist

    def DTWDistance(self, s1, s2, w=None):
        '''
        Calculates dynamic time warping Euclidean distance between two
        sequences. Option to enforce locality constraint for window w.
        '''
        DTW = {}

        if w:
            w = max(w, abs(len(s1) - len(s2)))

            for i in range(-1, len(s1)):
                for j in range(-1, len(s2)):
                    DTW[(i, j)] = float('inf')

        else:
            for i in range(len(s1)):
                DTW[(i, -1)] = float('inf')
            for i in range(len(s2)):
                DTW[(-1, i)] = float('inf')

        DTW[(-1, -1)] = 0

        for i in range(len(s1)):
            if w:
                for j in range(max(0, i - w), min(len(s2), i + w)):
                    dist = (s1[i] - s2[j]) ** 2
                    DTW[(i, j)] = dist + min(DTW[(i - 1, j)], DTW[(i, j - 1)], DTW[(i - 1, j - 1)])
            else:
                for j in range(len(s2)):
                    dist = (s1[i] - s2[j]) ** 2
                    DTW[(i, j)] = dist + min(DTW[(i - 1, j)], DTW[(i, j - 1)], DTW[(i - 1, j - 1)])

        return np.sqrt(DTW[len(s1) - 1, len(s2) - 1])

    def LB_Keogh(self, s1, s2, r):
        '''
        Calculates LB_Keough lower bound to dynamic time warping. Linear
        complexity compared to quadratic complexity of dtw.
        '''
        LB_sum = 0
        for ind, i in enumerate(s1):

            lower_bound = min(s2[(ind - r if ind - r >= 0 else 0):(ind + r)])
            upper_bound = max(s2[(ind - r if ind - r >= 0 else 0):(ind + r)])

            if i > upper_bound:
                LB_sum = LB_sum + (i - upper_bound) ** 2
            elif i < lower_bound:
                LB_sum = LB_sum + (i - lower_bound) ** 2

        return np.sqrt(LB_sum)

    def sc_score(self, data):
        s_lst = []
        for key, value in self.assignments.items():
            print(key, value)
            for item in value:
                a = 0
                iter = 0
                for mate in value:
                    dist_temp = self.merge_dis(data[item], data[mate], 10)
                    a = a + dist_temp
                    iter = iter + 1
                a = a / (iter - 1)
                
                b_lst = []
                for cent, cent_value in self.centroids.items():
                    if cent == key:
                        continue
                    dist_temp = self.merge_dis(data[item], cent_value, 10)
                    b_lst.append(dist_temp)
                b = min(b_lst)

                s = (b - a) / max(a, b)
                print(s)
                s_lst.append(s)
        s = np.mean(s_lst)
        print("SC", s)


    def cp_score(self, data, clu, clusterRes, keys, k):
        keys_lst = keys.tolist()
        cp_lst = []
        for i in range(1, k + 1):
            idx = np.where(clusterRes == i)
            cen = clu[i - 1]
            dis_sum = 0
            for j in idx[0]:
                dis_sum = dis_sum + self.merge_dis(cen, data[keys_lst[j]])
            cp_i = dis_sum / len(idx)
            # print(cp_i)
            cp_lst.append(cp_i)
        cp = np.average(cp_lst)
        print("CP_score", cp)
        return cp


if __name__ == '__main__':
    with open('dataset/all_data.csv', 'r') as file:
        reader = csv.reader(file)
        test = []
        for row in reader:
            test.append(row[1:-1])
        data = np.asarray(test).astype(float)
        print(data)
        test = ts_cluster(5)
        test.k_means_clust(data, 10, 20, 4)
        test.sc_score(data)
        centroids = test.get_centroids()
        # assignments = test.get_assignments()
        # sc_score = test.sc_score()
        for i in centroids.values():
            plt.plot(i)

        plt.show()
