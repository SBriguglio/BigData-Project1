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


def test(support=0.01):
    x = [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    y_a_1 = []
    y_pcya_1 = []
    y_pcyb_1 = []
    y_pcyc_1 = []
    for i in x:
        s = 0.01 * i
        try:
            # initialize
            p = APriori.APriori(sample_size=s, support=support)
            a = PCY.PCY(sample_size=s, support=support)
            # test a-priori
            p.a_priori()
            y_a_1.append(p.runtime)
            # test PCY
            a.pcyA()
            y_pcya_1.append(a.runtime)
            # test multistage
            a.pcyB()
            y_pcyb_1.append(a.runtime)
            # test multihash
            a.pcyC()
            y_pcyc_1.append(a.runtime)
        except IndexError:
            print("An error occurred")
    plt.plot(x, y_a_1, label="A-Priori")
    plt.plot(x, y_pcya_1, label="PCY")
    plt.plot(x, y_pcyb_1, label="Multistage")
    plt.plot(x, y_pcyc_1, label="Multihash")
    plt.xlabel("Dataset Size (%)")
    plt.ylabel("Run time (s)")
    plt.title("Support Threshold {}%".format(support * 100))
    plt.legend()
    plt.show()


if __name__ == '__main__':
    # Support Threshold = 1%
    start = time.time()
    t_start = start
    test(0.01)
    end = time.time()
    print('\x1b[6;30;42m' + "RUNTIME 1%: {}".format(end-start) + '\x1b[0m')
    # Support Threshold = 5%
    start = time.time()
    test(0.05)
    end = time.time()
    print('\x1b[6;30;42m' + "RUNTIME 5%: {}".format(end-start) + '\x1b[0m')
    # Supper Threshold = 10%
    start = time.time()
    test(0.1)
    end = time.time()
    print('\x1b[6;30;42m' + "RUNTIME 10%: {}".format(end-start) + '\x1b[0m')
    print("Done")
    t_end = time.time()
    print('\x1b[6;30;42m' + "TOTAL RUNTIME: {}".format(t_end-t_start) + '\x1b[0m')
