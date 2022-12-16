#!/usr/bin/env python

from collections import Counter


class Language:
    def __init__(self, name: str):
        self.name = name
        self.count = Counter()

    def __repr__(self) -> str:
        return self.name

    def train(self, file: str):
        """Train the Language with a text"""
        with open(file, "r") as f:
            for line in f.readlines():
                self.count["\\n"] += 1
                for char in line[:-1]:
                    self.count[char] += 1
            f.close()

    def save_count_as_txt(self):
        with open(self.name + "_count.txt", "w") as f:
            for key, val in self.count.items():
                f.write(key + ", " + str(val) + "\n")
            f.close()

    def load_count_txt(self, file: str):
        with open(file, "r") as f:
            for line in f.readlines():
                key, val = line.split(", ")
                self.count[key] += int(val)
            f.close()
