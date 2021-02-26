'''
Created by Spencer Briguglio
COMP 4250 Project 1
'''

import APriori
import PCY
import linecache
import random
import time
import matplotlib.pyplot as plt


if __name__ == '__main__':
    x = [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    y = []

    """
    for i in x:
        n = 0.01 * i
        print(n)
        try:
            a = APriori.APriori(sample_size=n)
            a.a_priori()
            y.append(a.runtime)
        except IndexError:
            print("An Error Occurred")

    plt.plot(x, y)
    plt.xlabel("Dataset Size (%)")
    plt.ylabel("Run time (ms)")
    plt.title("Support Threshold 1%")
    plt.show()
    """

    p = PCY.PCY()

    print("Done")
