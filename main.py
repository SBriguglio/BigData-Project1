import linecache
import random
import numpy as np


class APriori:
    def __init__(self, filename="retail.txt", sample_size=0.1, support=0.01):
        self.sample_size = sample_size
        self.filename = filename
        self.file = None
        self.n_buckets = 0
        self.n_sample_buckets = None
        self.max_int = 0
        self.support = support
        self.s = 0
        self.selected_baskets = []
        self.freq_item_table = []
        self.pairs_tri_matrix = []

        self.open_file()
        self.set_n_buckets()
        self.set_n_sample_buckets()
        self.set_s()
        self.choose_selected_baskets()

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
        for i in range(0, n):
            while True:
                random.seed()
                b = random.randint(0, self.n_buckets - 1)
                if not self.selected_baskets.__contains__(b):
                    self.selected_baskets.append(b+1)
                    break
        if len(self.selected_baskets) == n:
            print("[!!] {} sample buckets select from {} buckets".format(self.n_sample_buckets, self.n_buckets))
        else:
            print("[!!] Bucket Selection Failure")
        self.selected_baskets.sort()

    def set_freq_item_table_length(self, n):
        self.freq_item_table = self.freq_item_table[:n] + [0]*(n - len(self.freq_item_table))

    def set_pairs_tri_matrix_length(self, n):
        self.pairs_tri_matrix = self.pairs_tri_matrix[:n] + [0]*(n - len(self.pairs_tri_matrix))

    def a_priori(self):
        fn = self.filename

        # Pass 1:
        for bucket in self.selected_baskets:
            line = map(int, linecache.getline(fn, bucket).split())
            for i in line:
                if self.max_int < i:
                    self.max_int = i
                    self.set_freq_item_table_length(self.max_int+1)
                self.freq_item_table[i] += 1
        for i in range(0, self.max_int):
            if self.freq_item_table[i] < self.s:
                self.freq_item_table[i] = 0

        # Pass 2:
        self.set_freq_item_table_length(int((self.max_int * (self.max_int-1))/2))
        for bucket in self.selected_baskets:
            print("BUCKET: {}".format(bucket))
            line = [l for l in map(int, linecache.getline(fn, bucket).split())]
            for i in line:
                print(i, end=" ")
            else:
                break






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    a = APriori()
    a.a_priori()
    print("Done")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
