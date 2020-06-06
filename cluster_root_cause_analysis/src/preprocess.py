import matplotlib.pylab as plt
import numpy as np
import csv
from fastsst import SingularSpectrumTransformation


def preprocess():
    with open("../datasets/granger_test.csv", 'r') as file:
        reader = csv.reader(file)
        data = []
        sst_data = []
        name = []
        for row in reader:
            np_row = np.array(row[1:-1]).astype(np.float)
            if (np_row == 0).all():
                continue
            sst = SingularSpectrumTransformation(win_length=30)
            score = sst.score_offline(np_row)
            name.append(row[0])
            data.append(np_row)
            sst_data.append(score)


        for ind, item in enumerate(data):
            plt.plot(item)
            plt.plot(sst_data[ind])
            plt.title(name[ind])
            plt.show()


if __name__ == '__main__':
    preprocess()