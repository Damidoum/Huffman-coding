#!/usr/bin/env python

from collections import Counter
import json
import argparse
from pathlib import Path


class Language:
    """Language class -> can generate huffman code"""

    def __init__(self, name: str) -> None:
        self.name = name
        self.count = Counter()
        self.code = {}

    def __repr__(self) -> str:
        return self.name

    def train(self, file: str) -> None:
        """Train the Language with a text, this will analyse the frequency of each caracters in the document"""
        with open(file, "r") as f:
            content = f.read()
            self.count += Counter(content)
            f.close()

    def save_count_as_json(self, file: str) -> None:
        """Saves the dictionary that contains the occurrences of each letter"""
        with open(file, "w") as f:
            json.dump(self.count, f)
            f.close()

    def load_count_json(self, file: str) -> None:
        """Allows you to load a dictionary with the occurrences of letters that already exist"""
        with open(file, "r") as f:
            self.count = json.load(f)
            f.close()

    def generate_code(self) -> None:
        """Generate the code to encode with huffman"""

        # Init the code dictionary and the count of each letter
        count_letters_copy = self.count.copy()
        self.code = {}

        while len(count_letters_copy) > 1:
            # we get the letters with the lower count and remove them from the count dictionary
            (l_inf, n_inf), (l_sup, n_sup) = count_letters_copy.most_common()[-1:-3:-1]
            del count_letters_copy[l_inf]
            del count_letters_copy[l_sup]

            # we are adding the sum of the two letters to the dictionary to continue the huffman graph
            count_letters_copy[l_inf + "\\" + l_sup] = n_inf + n_sup

            for char in l_inf.split("\\"):
                # adding a 0 to the weakest letters
                self.code[char] = "0" + self.code.get(char, "")
            for char in l_sup.split("\\"):
                # adding a 1 to the strongest letters
                self.code[char] = "1" + self.code.get(char, "")

    def save_code(self, file) -> None:
        """Save the code in a file"""
        with open(file, "w") as f:
            data = str(self.code)
            f.write(data)
            f.close()


# New Language : english
english = Language("english")
french = Language("français")
deutsch = Language("german")
language = {"english": english, "french": french, "deutsch": deutsch}

if __name__ == "__main__":

    # Creating an arguments parser
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--coder", "-c")
    parser.add_argument("--language", "-l", default="english")
    parser.add_argument("-f", "--freq", default=False, action="store_true")
    args = parser.parse_args()

    # Train the Language -> counting letters
    language[args.language].train(args.file)

    if args.coder != None:
        english.generate_code()
        english.save_code(args.coder)
    else:
        name_file = "output/codes/" + str(Path(args.file).stem) + ".coder"
        english.generate_code()
        english.save_code(name_file)

    if args.freq:
        print(language[args.language].code)
