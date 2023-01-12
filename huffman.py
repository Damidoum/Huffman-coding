#!/usr/bin/env python


import argparse
from pathlib import Path
from utilities import (
    int_to_bytes,
    bytes_to_int,
    decode,
    get_code_from_file,
    which_reader,
    which_writer,
    how_many_bits_more,
)


def encode_file(file: str, huf_dic: dict, output: str, bin: bool) -> None:
    """Encoding a file"""
    code = huf_dic.copy()  # copy the code of the letters
    output_file = open(output, which_writer(bin))  # open the output file
    encoded = ""
    with open(file, "r") as f:
        for line in f.readlines():
            for letter in line:
                # converting the letter into string of 0 and 1
                encoded += code[letter]
        f.close()
    if not bin:
        output_file.write(encoded)
    else:
        l = len(encoded)
        additionals_bits = how_many_bits_more(l)
        encoded = additionals_bits * "0" + encoded
        for k in range(0, l + additionals_bits, 8):
            seq = encoded[k : k + 8]  # we group 0 and 1 by 8
            output_file.write(bytes_to_int(seq).to_bytes(1))

        # we need to know how many bits need to be removed
        output_file.write(additionals_bits.to_bytes(1))

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

        # get the last byte, tells us how many bits are important in the penultimate byte
        additional_bits = bytes_to_int(encoded[-8:])
        encoded = encoded[:-8]  # remove this last byte
        # only keep the right number of bits on the first byte
        encoded = encoded[additional_bits:]

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
        if args.output == None:
            output = "output/huf/" + str(Path(args.file).stem) + ".huf"
        else:
            output = args.output
        encode_file(args.file, code, output, args.bin)

    else:
        # we are decoding
        if args.output == None:
            output = "output/decoded/" + str(Path(args.file).stem) + ".txt"
        else:
            output = args.output
        decode_file(args.file, code, output, args.bin)
