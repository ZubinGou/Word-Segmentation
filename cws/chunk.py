#!usr/bin/env python
#-*- coding:utf-8 -*-

import math


class Chunk:
    def __init__(self, words: list, freqs: list):
        self.words = words
        self.lens = map(lambda x: len(x), words)
        self.length = sum(self.lens)
        self.mean = float(self.length) / len(words)
        self.var = sum(map(lambda x: (x - self.mean) ** 2, self.lens)) / len(self.words)
        self.entropy = sum([math.log(float(freqs[x])) for x in words if len(x) == 1 and x in freqs])

    def __lt__(self, other):
        return (self.length, self.mean, -self.var, self.entropy) < (other.length, other.mean, -other.var, other.entropy)

    def __str__(self):
        return ' '.join(self.words)
