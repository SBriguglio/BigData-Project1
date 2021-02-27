import linecache
import random
import time
import numpy as np
import math
from bitarray import bitarray


def getPrimes(limit):
    prime_list = []
    numbers = [True] * limit
    for i in range(2, limit):
        if numbers[i]:
            prime_list.append(i)
            for n in range(i ** 2, limit, i):
                numbers[n] = False

    max_dist = math.inf
    numb = 0
    for p in prime_list:
        if abs(n - p) < max_dist:
            max_dist = abs(n - p)
            numb = p

    return numb


class PCY:
    def __init__(self, support=0.01, filename="retail.txt", sample_size=0.1):
        self.sample_size = sample_size
        self.filename = filename
        self.file = None
        self.n_buckets = 0
        self.n_sample_buckets = None
        self.max_int = 0
        self.hash_prime = 1
        self.hash_prime_2 = 2
        self.support = support
        self.s = 0
        self.selected_baskets = []
        self.freq_item_table = [0]
        self.freq_items = []
        self.freq_pairs_list = {}
        self.bucket_hash = None
        self.bitmap = None
        self.bitmap_2 = None
        self.runtime = 0

        self.open_file()
        self.set_n_buckets()
        self.set_n_sample_buckets()
        self.set_s()
        self.choose_selected_baskets()
        self.set_max_int()
        self.set_hash_prime()
        self.set_hash_prime_2()
        self.set_bitmap_size()
        self.set_bitmap_2_size()
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
        self.s = int(self.n_sample_buckets * self.support)

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

    def set_max_int(self):
        fn = self.filename
        for basket in self.selected_baskets:
            line = map(int, linecache.getline(fn, basket).split())
            for i in line:
                if self.max_int < i:
                    self.max_int = i
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
        n = int(self.max_int+50)
        prime = getPrimes(n)
        self.hash_prime = prime
        print("hash_prime = {}".format(self.hash_prime))

    def set_hash_prime_2(self):
        """
        I am using this method just to choose a prime number close to the maximum number found in data.
        This method is largely an adaptation of one found on stack overflow to find nearest primes using the Sieve of
        Eratosthenes method.
        It can be found here: https://stackoverflow.com/questions/58680930/closest-prime-number-in-python
        """
        n = int((self.max_int/2)+50)
        prime = getPrimes(n)
        self.hash_prime_2 = prime
        print("hash_prime_2 = {}".format(self.hash_prime_2))

    def hash_a(self, i, j):
        return (i*j+j-i) % self.hash_prime

    def hash_b(self, i, j):
        return (i**2 + i**2 - j) % int(self.hash_prime_2)

    def set_bitmap_size(self):
        """
        At the moment, the smallest addressable datatype in python is 8-bits long.
        A proper array of bits can be made using the bitarray package imported above.
        """
        self.bitmap = bitarray(self.hash_prime)
        self.bitmap.setall(0)

    def set_bitmap_2_size(self):
        self.bitmap_2 = bitarray(self.hash_prime_2)
        self.bitmap_2.setall(0)

    def pcyA(self, verbose=0):
        fn = self.filename
        # Pass 1:
        start_time = time.time()
        self.bucket_hash = np.zeros(self.hash_prime, np.int32)
        for basket in self.selected_baskets:
            line = list([l for l in map(int, linecache.getline(fn, basket).split())])
            length = len(line)
            # update frequency of the item if the bucket only contains a singleton, skip the rest
            if length == 0:
                pass
            elif length == 1:
                try:
                    self.freq_item_table[line[0]] += 1
                except IndexError:
                    print("[!!] IndexError: (A) i of the index. i = {}".format(line[0]))
            else:
                for i in range(0, length-1):
                    # updating item frequency
                    try:
                        self.freq_item_table[line[i]] += 1  # Kept getting list index out of range error here
                    except IndexError:
                        print("[!!] IndexError: (B) i of the index. i = {}".format(line[i]))

                    # hashing pair to bucket and updating bucket count
                    for j in range(i+1, length):
                        try:
                            self.bucket_hash[self.hash_a(i, j)] += 1
                        except IndexError:  # checking for index error
                            print("[!!] IndexError: i in bucket_hash: {}\
                            \n length of bucket_hash: {}".format(self.hash_a(i, j), self.bucket_hash.shape))

                # incrementing the frequency of the last item in the basket
                try:
                    self.freq_item_table[line[length-1]] += 1  # Kept getting list index out of range error here
                except IndexError:
                    print("[!!] IndexError: (C) i of the index. i = {}".format(line[length-1]))
        # close file as it is no longer needed
        self.close_file()

        # Hash Frequent Pairs to BitMap, get rid of old buckets
        for b in range(0, self.hash_prime):
            if self.bucket_hash[b] >= self.s:
                self.bitmap[b] = 1

        # Create Frequent-Pair Count Table (containing all candidate pairs and their counts)
        for i in range(0, self.max_int-1):
            if self.freq_item_table[i] >= self.s:
                self.freq_items.append(i)
                for j in range(i+1, self.max_int):
                    if self.freq_item_table[j] >= self.s:
                        h = self.hash_a(i, j)
                        if self.bitmap[h] == 1:
                            self.freq_pairs_list[(i, j)] = self.bucket_hash[h]
        # Need to append high item outside of loop because cannot efficiently be done within
        if self.freq_item_table[self.max_int] >= self.s:
            self.freq_items.append(self.max_int)

        # free hash table for pairs and Item Counts table
        self.bucket_hash = None
        self.freq_item_table = None

        # end of run time
        end_time = time.time()

        self.runtime = end_time - start_time

        # this just prints the frequent pairs, so it is not measured in run time
        if verbose == 2:
            for p in self.freq_pairs_list:
                print("Pair: {}    Frequency: {}".format(p, self.freq_pairs_list[p]))
        if verbose == 1:
            print("[PCY]\n|  Frequent Pairs: {} Run time: {}".format(len(self.freq_pairs_list), self.runtime))

        # Note that because this method (pcyA) updates the PCY object's bitmap, candidate pair count dictionary and
        # frequent item list, the multistage and multihash method (below) will simply call upon this method.

    def pcyB(self, verbose=0, a_verbose=0):
        self.pcyA(verbose=a_verbose)
        self.bucket_hash = np.zeros(int(self.hash_prime_2), np.int32)
        # start of run time
        start_time = time.time()

        # rehash all frequent pairs to new hashtable
        for i in self.freq_pairs_list:
            h = self.hash_b(i[0], i[1])
            self.bucket_hash[h] += self.freq_pairs_list[i]

        # reduce hashtable to bitmap ONLY accepting frequent buckets
        index = 0
        for b in self.bucket_hash:
            if b >= self.s:
                self.bitmap_2[index] = 1
            index += 1

        # remove candidate pairs that aren't frequent by removing those which do not hash to frequent bucket in bitmap
        freq_pairs = {}
        for i in self.freq_pairs_list:
            h = self.hash_b(i[0], i[1])
            if self.bitmap_2[h] == 1:
                freq_pairs[i] = self.freq_pairs_list[i]
        self.freq_pairs_list = freq_pairs

        # end of run time
        end_time = time.time()
        self.runtime += end_time - start_time

        # print frequent pairs
        if verbose == 2:
            for p in self.freq_pairs_list:
                print("Pair: {}    Frequency: {}".format(p, self.freq_pairs_list[p]))
        if verbose == 1:
            print("[Multistage]\n|  Frequent Pairs: {} Run time: {}".format(len(self.freq_pairs_list), self.runtime))
