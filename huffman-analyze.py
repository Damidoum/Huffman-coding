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
