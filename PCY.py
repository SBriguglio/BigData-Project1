import linecache
import random
import time
import matplotlib.pyplot as plt
import numpy as np
import math
from bitarray import bitarray


class PCY:
    def __init__(self, support=0.01, filename="retail.txt", sample_size=0.1):
        self.sample_size = sample_size
        self.filename = filename
        self.file = None
        self.n_buckets = 0
        self.n_sample_buckets = None
        self.max_int = 0
        self.hash_prime = 1
        self.support = support
        self.s = 0
        self.selected_baskets = []
        self.freq_item_table = [0]
        self.freq_pairs_list = {}
        self.bucket_hash = None
        self.bitmap = None
        self.runtime = 0

        self.open_file()
        self.set_n_buckets()
        self.set_n_sample_buckets()
        self.set_s()
        self.choose_selected_baskets()
        self.set_max_int()  # <-- Error Here (Calls Line 82)
        self.set_hash_prime()
        self.set_bitmap_size()
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

    def set_max_int(self): # Needs to be tested
        fn = self.filename
        for line in self.selected_baskets:
            a = map(int, linecache.getline(fn, line).split())
            for i in a:
                if self.max_int < line[i]:
                    self.max_int = line[i]
                    self.set_freq_item_table_length(self.max_int + 1)
        # Can remove after testing
        print("Max_int = {}".format(self.max_int))

    def set_hash_prime(self):
        """
        I am using this method just to choose a prime number close to the maximum number found in data.
        This method is largely an adaptation of one found on stack overflow to find nearest primes using the Sieve of
        Eratosthenes method.
        It can be found here: https://stackoverflow.com/questions/58680930/closest-prime-number-in-python
        """
        def getPrimes(limit):
            prime_list = []
            numbers = [True] * limit
            for i in range(2, limit):
                if numbers[i]:
                    prime_list.append(i)
                    for n in range(i ** 2, limit, i):
                        numbers[n] = False
            return prime_list

        number = self.max_int
        primes = getPrimes(number + number*1.5)
        max_dist = math.inf
        numb = 0
        for p in primes:
            if abs(number - p) < max_dist:
                max_dist = abs(number - p)
                numb = p

        self.hash_prime = numb

    def hash_a(self, i, j):
        return (i*j) % self.hash_prime

    def set_bitmap_size(self):
        """
        At the moment, the smallest addressable datatype in python is 8-bits long.
        A proper array of bits can be made using the bitarray package imported above.
        """
        self.bitmap = bitarray(self.hash_prime)
        self.bitmap.setall(0)

    def pcyA(self):
        fn = self.filename

        # Pass 1:
        start_time = time.time()
        self.bucket_hash = np.zeros(self.hash_prime, np.int32)
        for basket in self.selected_baskets:
            line = list([l for l in map(int, linecache.getline(fn, basket).split())])
            length = len(line)
            for i in range(0, length-1):
                try:
                    self.freq_item_table[line[i]] += 1  # Kept getting list index out of range error here
                except IndexError:
                    print("[!!] IndexError: i of the index. i = {}".format(line[i]))

                for j in range(i+1, length):  # hashing each pair in the basket and incrementing the bucket hashed too
                    try:
                        self.bucket_hash[self.hash_a(i, j)] += 1
                    except IndexError:  # checking for index error
                        print("[!!] IndexError: i in bucket_hash: {}\
                        \n length of bucket_hash: {}".format(self.hash_a(i, j), self.bucket_hash.shape))

            try:  # Not incrementing frequency of last element in the basket in the above for-loops, it is done here
                self.freq_item_table[line[length-1]] += 1  # Kept getting list index out of range error here
            except IndexError:
                print("[!!] IndexError: i of the index. i = {}".format(line[length-1]))
        self.close_file()

        # Hash Frequent Pairs to BitMap, get rid of old buckets
        for b in range(0, self.hash_prime):
            if self.bucket_hash[b] >= self.s:
                self.bitmap[b] = 1
        self.bucket_hash = None

        # Pass 2
        for i in range(0, self.hash_prime-1):
            for j in range(i+1, self.hash_prime):
                h = self.hash_a(i, j)
                if self.bitmap[h] == 1:
                    if self.freq_pairs_list.__contains__((i, j)):
                        self.freq_pairs_list[(i, j)] += 1
                    else:
                        self.freq_pairs_list[(i, j)] = 1

        # end of run time
        end_time = time.time()
        self.runtime = end_time - start_time

        # this just prints the frequent pairs, so it is not measured in run time
        for p in self.freq_pairs_list:
            print("Pair: {}    Frequency: {}".format(p, self.freq_pairs_list[p]))
