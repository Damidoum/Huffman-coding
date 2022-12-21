#!/usr/bin/env python

from collections import Counter
import json


class Language:
    def __init__(self, name: str):
        self.name = name
        self.count = Counter()

    def __repr__(self) -> str:
        return self.name

    def train(self, file: str):
        """Train the Language with a text"""
        with open(file, "r") as f:
            content = f.read()
            self.count += Counter(content)
            f.close()

    def save_count_as_json(self, file: str):
        with open(file, "w") as f:
            json.dump(self.count, f)
            f.close()

    def load_count_json(self, file: str):
        with open(file, "r") as f:
            self.count = json.load(f)
            f.close()


def huffman(count_characters: Counter) -> dict:
    count_characters_copy = count_characters.copy()
    code = {}

    while len(count_characters_copy) > 1:
        (l_inf, n_inf), (l_sup, n_sup) = count_characters_copy.most_common()[-1:-3:-1]
        del count_characters_copy[l_inf]
        del count_characters_copy[l_sup]
        count_characters_copy[l_inf + " " + l_sup] = n_inf + n_sup
        for char in l_inf.split(" "):
            code[char] = "0" + code.get(char, "")
        for char in l_sup.split(" "):
            code[char] = "1" + code.get(char, "")
    return code


english = Language("english")
english.train("../python-eval-groupe1/sample-01.txt")
print(huffman(english.count))
