#!/usr/bin/env python

from collections import Counter
import json
import argparse
from pathlib import Path
from utilities import how_many_bits_more


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

    def save_huff_graph(self, output_file: str, bin: bool):
        """save the huff graph in a file (binary file if the option is True)"""
        huf_dic = self.code
        if not bin:
            # saving in a text file
            with open(output_file, "w") as f:
                data = str(huf_dic)
                f.write(data)
                f.close()
        else:
            # saving in a binary file
            with open(output_file, "wb") as f:
                for key, val in huf_dic.items():
                    key_utf8 = bytes(key, "utf-8")  # the key in the format utf-8
                    # to decode we need to know how many bytes we use to encode the key
                    f.write(len(key_utf8).to_bytes(1))
                    f.write(key_utf8)  # encoding the key (letter)

                    """to encode the value, we adopt the following scheme: 
                    - a first byte to know how many bytes are necessary to encode the value
                    - then the binary code of the value
                    - a last byte to know how many artificial 0s have been added in the first byte of the value (to fill the byte)
                    (see utilities.how_many_bits_more for more explanation)
                    
                    ex for the val 1000011100 : 
                    - 10 bits -> we need 2 bytes, so we encode 2 : 00000010
                    - then we encode the val in 2 bytes: 00000010 00011100
                    - in the first byte we have 6 additional 0s so we encode 6 : 00000110
                    return -> 00000010 00000010 00011100 00000110"""

                    how_many_bytes = len(val) // 8 + int(
                        bool(len(val) % 8)
                    )  # number of bytes required to encode the val
                    last_byte = how_many_bits_more(len(val)).to_bytes(1)
                    f.write(how_many_bytes.to_bytes(1))
                    f.write(int(val, 2).to_bytes(how_many_bytes))  # encoding the val
                    f.write(last_byte)


# New Language : english
english = Language("english")

if __name__ == "__main__":

    # Creating an arguments parser
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name")
    parser.add_argument("--coder", "-c", help="choose the output file name")
    parser.add_argument(
        "-b",
        "--bin",
        default=False,
        action="store_true",
        help="save the graph in a bin file",
    )
    args = parser.parse_args()

    # Train the Language -> counting letters
    english.train(args.file_name)

    if args.coder != None:
        english.generate_code()
        english.save_huff_graph(args.coder, args.bin)
    else:
        name_file = "huffman_graph/" + str(Path(args.file_name).stem) + ".coder"
        english.generate_code()
        english.save_huff_graph(name_file, args.bin)
