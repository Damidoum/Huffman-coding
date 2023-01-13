#!/usr/bin/env python


import argparse
from pathlib import Path
from utilities import (
    int_to_bytes,
    decode,
    read_huff_graph,
    which_reader,
    which_writer,
    how_many_bits_more,
)


def encode_file(
    file_name: str, huf_dic: dict, output_file_name: str, bin: bool
) -> None:
    """Encode a file
    parameters :
    - file_name : the name of the file we want to encode
    - huf_dic : the dictionary we want to use to encode
    - output_file_name : in which file the code will be save
    - bin : True if we want to encode in a bin file, False if not
    """
    code = huf_dic.copy()  # copy the code of the letters
    output_file = open(output_file_name, which_writer(bin))  # open the output file
    encoded = ""
    with open(file_name, "r") as f:
        for line in f.readlines():
            for letter in line:
                # converting the letter into string of 0 and 1
                encoded += code[letter]
        f.close()
    if not bin:
        # we are not encoding in a bin file, it's easy
        output_file.write(encoded)
    else:
        # we are encoding in a bin file
        l = len(encoded)
        # if l is not a multiple of 8 we need to add bits
        additionals_bits = how_many_bits_more(l)
        # we add these bits at the beginnig of the chain
        encoded = additionals_bits * "0" + encoded
        for k in range(0, l + additionals_bits, 8):
            seq = encoded[k : k + 8]  # we group 0 and 1 by 8 (byte)
            output_file.write(int(seq, 2).to_bytes(1))

        # we need to know how many bits need to be removed, we write this information at the end
        output_file.write(additionals_bits.to_bytes(1))

    output_file.close()


def decode_file(
    encoded_file_name: str, huf_dic: dict, output_file_name: str, bin: bool
) -> None:
    """Decode an encoded file
    parameters :
    - encoded_file_name : the name of the encoded file
    - huf_dic : the dictionary we want to use to decode
    - output_file_name : in which file the decoded text will be save
    - bin : True if we want to decode a bin file, False if not"""

    # To decode we need to swap keys and values of the dictionary
    code = {v: k for k, v in huf_dic.items()}

    with open(encoded_file_name, which_reader(bin)) as f:
        encoded_string = f.read()  # saving the encoded sequence in a str
        f.close()

    if not bin:
        # easy case, no need to transform the str
        encoded = encoded_string
    else:
        # extract from a bin file, we need to remove the artificial bits that we have added
        encoded = ""  # the results

        for k in list(encoded_string):
            encoded += int_to_bytes(k)  # converting int into seq of 0 and 1

        # get the last byte, tells us how many bits are important in the first byte
        additional_bits = int(encoded[-8:], 2)
        encoded = encoded[:-8]  # remove the last byte
        # only keep the right number of bits on the first byte
        encoded = encoded[additional_bits:]

    decoded = decode(encoded, code)  # using decode function from utilities.py

    # writing the result in a file
    with open(output_file_name, "w") as f:
        f.write(decoded)
        f.close()


if __name__ == "__main__":
    # creating argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument(
        "--decode",
        "-d",
        default=False,
        action="store_true",
        help="use this parameter if you want to decode",
    )
    parser.add_argument("--output", "-o", help="choose the output file name")
    parser.add_argument(
        "--coder",
        "-c",
        default="huffman_graph/english.coder",
        help="choose the huff graph, default : huffman_graph/english.coder",
    )
    parser.add_argument(
        "--bin",
        "-b",
        default=False,
        action="store_true",
        help="encode in a bin file or decode a bin file",
    )
    parser.add_argument(
        "--huff_graph_bin",
        "-hufb",
        default=False,
        action="store_true",
        help="use this parameter if the huff graph you want to use is store in a bin file",
    )
    args = parser.parse_args()

    # get code of each letter
    huf_dic = read_huff_graph(args.coder, args.hufb)

    if not args.decode:
        # we are encoding
        if args.output == None:
            output = (
                "output/huf/" + str(Path(args.file).stem) + args.bin * "_bin" + ".huf"
            )
        else:
            output = args.output
        encode_file(args.file, huf_dic, output, args.bin)

    else:
        # we are decoding
        if args.output == None:
            output = "output/decoded/" + str(Path(args.file).stem) + ".txt"
        else:
            output = args.output
        decode_file(args.file, huf_dic, output, args.bin)
