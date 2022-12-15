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
        with open(file, "r") as file:
            for line in file.readlines():
                self.count["\n"] += 1
                for char in line[:-1]:
                    self.count[char] += 1
            file.close()

    def save_count_as_txt(self):
        with open(self.name + "_count.txt", "w") as file:
            for key, val in self.count.items():
                file.write(key + " " + str(val) + "\n")
            file.close()
