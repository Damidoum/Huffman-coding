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


def encode_file_bin(file: str, dic: dict, output: str) -> None:
    """Encoding a file in a binary file"""
    code = dic.copy()  # copy the code of the letters
    output_file = open(output, "wb")  # open the output file
    encoded = ""
    with open(file, "r") as f:
        for line in f.readlines():
            for letter in line[:-1]:
                encoded += code[letter]
            encoded += code["\n"]
        f.close()
    for k in range(0, len(encoded) - len(encoded) % 8, 8):
        seq = encoded[k : k + 8]
        num = 0
        for k in range(8):
            num += int(seq[k]) * (2 ** (7 - k))
        output_file.write(num.to_bytes(1))

    # last byte
    l = len(encoded) % 8
    seq = encoded[len(encoded) - l :]
    num = 0
    for k in range(len(seq)):
        num += int(seq[k]) * (2 ** (7 - k))
    output_file.write(num.to_bytes(1))

    # we need to know how many bit are important in the last byte. We encode this number (which is l) in an other byte.
    output_file.write(l.to_bytes(1))
    output_file.close()


def int_to_byteString(n: int) -> str:
    """convert integer into a string representing his byte writing"""
    seq = str(bin(n))[2:]
    l = len(seq)
    return (8 - l) * "0" + seq


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


def decode_file_bin(encoded_file: str, dic: dict, output_file: str) -> None:
    """decode an encoded binary file"""
    # for decoding we need to swap keys and values of the dictionary
    code = {v: k for k, v in dic.items()}

    with open(encoded_file, "rb") as f:
        encode_bin = f.read()
        f.close()

    # we want to convert these byte into string of 0 and 1
    encoded = ""
    for byte in list(encode_bin):
        encoded += int_to_byteString(byte)
    l = encoded[-8:]
    encoded = encoded[:-8]
    num = 0
    for k in range(8):
        num += int(l[k]) * (2 ** (7 - k))
    encoded = encoded[: -8 + num]

    decode = ""  # decoded text

    # we try to find wich sequence of 0 and 1 we are reading
    while len(encoded) > 0:
        key = ""
        count = 1
        possibilities = (
            code.keys()
        )  # differents possibilites of sequence, at the beging all sequence are possibled

        while len(possibilities) > 1:
            # at each passage in the loop we reduce the possibilities by looking at the next character of the file
            for char in encoded:
                key += char
                # update possibilities
                possibilities = [x for x in possibilities if x[:count] == key]
                count += 1
                if len(possibilities) == 1:
                    break
        encoded = encoded[len(key) :]
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
    parser.add_argument("--bin", "-b", default=False, action="store_true")
    args = parser.parse_args()

    # get code of each letter
    code = get_code_from_file(args.coder)

    if not args.decode:
        # we are encoding
        if not args.bin:
            # not in a bin file
            if args.output == None:
                output = "output/huf/" + str(Path(args.file).stem) + ".huf"
            else:
                output = args.output
            encode_file(args.file, code, output)
        else:
            # in a bin file
            if args.output == None:
                output = "output/bin/" + str(Path(args.file).stem) + ".huf"
            else:
                output = args.output
            encode_file_bin(args.file, code, output)

    else:
        # we are decoding
        if not args.bin:
            # not in a bin file
            if args.output == None:
                output = "output/huf/" + str(Path(args.file).stem) + ".txt"
            else:
                output = args.output
            decode_file(args.file, code, output)
        else:
            # in a bin file
            if args.output == None:
                output = "output/bin/" + str(Path(args.file).stem) + ".txt"
            else:
                output = args.output
            decode_file_bin(args.file, code, output)
