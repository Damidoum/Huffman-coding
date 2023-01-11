#!/usr/bin/env python


import argparse
from pathlib import Path
from utilities import (
    int_to_bytes,
    bytes_to_int,
    decode,
    get_code_from_file,
    which_reader,
)


def encode_file(file: str, huf_dic: dict, output: str) -> None:
    """Encoding a file"""
    code = huf_dic.copy()  # copy the code of the letters
    output_file = open(output, "w")  # open the output file
    with open(file, "r") as f:
        for line in f.readlines():
            for letter in line[:-1]:
                output_file.write(code[letter])
            output_file.write(code["\n"])
        f.close()
    output_file.close()


def encode_file_bin(file: str, huf_dic: dict, output: str) -> None:
    """Encoding a file in a binary file"""
    code = huf_dic.copy()  # copy the code of the letters
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


def decode_file(encoded_file: str, huf_dic: dict, output_file: str, bin: bool) -> None:
    """decode an encoded file"""
    # for decoding we need to swap keys and values of the dictionary
    code = {v: k for k, v in huf_dic.items()}

    with open(encoded_file, which_reader(bin)) as f:
        encoded_string = f.read()
        f.close()

    if bin:
        # we need to modify a little bit the data
        encoded = ""  # content of the encoded file
        for k in list(encoded_string):
            encoded += int_to_bytes(k)

        last_byte = encoded[
            -8:
        ]  # get the last byte, tells us how many bits are important in the penultimate byte
        encoded = encoded[:-8]  # remove the last byte
        encoded = encoded[
            : -8 + bytes_to_int(last_byte)
        ]  # only keep the right number of bits on the penultimate byte

    else:
        encoded = encoded_string

    decoded = decode(encoded, code)

    # writing the result in a file
    with open(output_file, "w") as f:
        f.write(decoded)
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
        if args.output == None:
            output = "output/decoded/" + str(Path(args.file).stem) + ".txt"
        else:
            output = args.output
        decode_file(args.file, code, output, args.bin)
