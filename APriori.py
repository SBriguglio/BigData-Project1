import linecache
import random
import time
import matplotlib.pyplot as plt


class APriori:
    def __init__(self, support=0.01, filename="retail.txt", sample_size=0.1):
        self.sample_size = sample_size
        self.filename = filename
        self.file = None
        self.n_buckets = 0
        self.n_sample_buckets = None
        self.max_int = 0
        self.support = support
        self.s = 0
        self.selected_baskets = []
        self.freq_item_table = [0]
        self.pairs_tri_matrix = []
        self.freq_pairs_list = []
        self.runtime = 0

        self.open_file()
        self.set_n_buckets()
        self.set_n_sample_buckets()
        self.set_s()
        self.choose_selected_baskets()
        print("Ready")

    def open_file(self):
        self.file = open(self.filename)

    def close_file(self):
        self.file.close()

    def set_n_buckets(self):
        f = self.file
        while f.readline():
            self.n_buckets += 1

    def set_n_sample_buckets(self):
        self.n_sample_buckets = int(self.n_buckets * self.sample_size)

    def set_s(self):
        self.s = int(self.n_buckets * self.support)

    def choose_selected_baskets(self):
        n = self.n_sample_buckets
        if self.sample_size != 1:
            for i in range(0, n):
                while True:
                    random.seed()
                    b = random.randint(0, self.n_buckets)  # - 1)
                    if not self.selected_baskets.__contains__(b):
                        self.selected_baskets.append(b + 1)
                        break
        else:
            for i in range(0, n):
                self.selected_baskets.append(i)
        if len(self.selected_baskets) == n:
            print("{} sample buckets select from {} buckets".format(self.n_sample_buckets, self.n_buckets))
        else:
            print("[!!] Bucket Selection Failure")
        self.selected_baskets.sort()

    def set_freq_item_table_length(self, n):
        self.freq_item_table = self.freq_item_table[:n] + [0] * (n - len(self.freq_item_table))

    def set_pairs_tri_matrix_length(self, n):
        self.pairs_tri_matrix = self.pairs_tri_matrix[:n] + [0] * (n - len(self.pairs_tri_matrix))

    def a_priori(self):
        fn = self.filename
        # Pass 1:
        start_time = time.time()
        for bucket in self.selected_baskets:
            line = map(int, linecache.getline(fn, bucket).split())
            for i in line:
                if self.max_int < i:
                    self.max_int = i
                    self.set_freq_item_table_length(self.max_int + 1)
                try:
                    self.freq_item_table[i] += 1  # Keep getting list index out of range error here
                except IndexError:
                    print("[!!] IndexError: i of the index. i = {}".format(i))
        for i in range(0, self.max_int):
            if self.freq_item_table[i] < self.s:
                self.freq_item_table[i] = 0

        # Pass 2:
        tri_mat_size = int((self.max_int * (self.max_int - 1)) / 2) + 1
        self.set_pairs_tri_matrix_length(tri_mat_size)
        for bucket in self.selected_baskets:
            line = list([l for l in map(int, linecache.getline(fn, bucket).split())])
            if len(line) > 1:
                for i in range(0, len(line)):
                    if (self.freq_item_table[line[i]] != 0) and (i != len(line) - 1):
                        for j in range(i + 1, len(line)):
                            if self.freq_item_table[line[j]] != 0:
                                k = line[i]
                                m = line[j]
                                index = int((k - 1) * (self.max_int - (k / 2))) + m - k
                                self.pairs_tri_matrix[index] += 1
                                if self.pairs_tri_matrix[index] >= self.s \
                                        and not self.freq_pairs_list.__contains__((k, m)):
                                    self.freq_pairs_list.append((k, m))

        # count run time
        end_time = time.time()
        self.runtime = end_time - start_time

        # not included in run time because not part of A-Priori algorithm. This just prints results.
        for i in self.freq_pairs_list:
            index = int((i[0] - 1) * (self.max_int - (i[0] / 2))) + i[1] - i[0]
            print("{}, {} : {}".format(i[0], i[1], self.pairs_tri_matrix[index]))
