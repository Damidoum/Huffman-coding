#!/usr/bin/env python


import argparse
from pathlib import Path


def get_code_from_file(file: str) -> dict:
    """import the code of each letter from a file"""
    dic = {}
    # reading the file to make dictionary
    with open(file, "r") as f:
        content = f.read()[1:-1].split(", ")
        for part in content:
            char = part.split(": ")
            key, val = char[0][1:-1], char[1][1:-1]
            dic[key] = val
        f.close()

    # replacing \\n by \n
    if "\\n" in dic.keys():
        dic["\n"] = dic["\\n"]
        del dic["\\n"]
    return dic


def encode_file(file: str, dic: dict, output: str) -> None:
    """Encoding a file"""
    code = dic.copy()  # copy the code of the letters
    output_file = open(output, "w")  # open the output file
    with open(file, "r") as f:
        for line in f.readlines():
            for letter in line[:-1]:
                output_file.write(code[letter])
            output_file.write(code["\n"])
        f.close()
    output_file.close()


def decode_file(encoded_file: str, dic: dict, output_file: str) -> None:
    """decode an encoded file"""
    # for decoding we need to swap keys and values of the dictionary
    code = {v: k for k, v in dic.items()}

    with open(encoded_file, "r") as f:
        encode = f.read()
        f.close()

    decode = ""  # decoded text

    # we try to find wich sequence of 0 and 1 we are reading
    while len(encode) > 0:
        key = ""
        count = 1
        possibilities = (
            code.keys()
        )  # differents possibilites of sequence, at the beging all sequence are possibled

        while len(possibilities) > 1:
            # at each passage in the loop we reduce the possibilities by looking at the next character of the file
            for char in encode:
                key += char
                # update possibilities
                possibilities = [x for x in possibilities if x[:count] == key]
                count += 1
                if len(possibilities) == 1:
                    break
        encode = encode[len(key) :]
        decode += code[key]

    # writing the result in a file
    with open(output_file, "w") as f:
        f.write(decode)
        f.close()


if __name__ == "__main__":
    # creating argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--decode", "-d", default=False, action="store_true")
    parser.add_argument("--output", "-o")
    parser.add_argument("--coder", "-c", default="output/codes/english.coder")
    args = parser.parse_args()

    # get code of each letter
    code = get_code_from_file(args.coder)

    if not args.decode:
        # we are encoding
        if args.output == None:
            output = "output/huf/" + str(Path(args.file).stem) + ".huf"
        else:
            output = args.output
        encode_file(args.file, code, output)

    else:
        # we are decoding
        if args.output == None:
            output = "output/huf/" + str(Path(args.file).stem) + ".txt"
        else:
            output = args.output
        decode_file(args.file, code, output)
