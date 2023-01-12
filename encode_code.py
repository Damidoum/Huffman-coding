from utilities import int_to_bytes, how_many_bits_more

dic = {"%": "100011110", "•": "01111011110011010001"}
# "|": "0111101111001101001"x


def write_char(char):
    b = bytes(char, "utf-8")
    return len(b).to_bytes(1), b


with open("test2.bin", "wb") as f:
    for key, val in dic.items():
        f.write(write_char(key)[0])
        f.write(write_char(key)[1])
        n_bytes = len(val) // 8 + int(bool(len(val) % 8))  # number of bytes
        last_byte = int_to_bytes(len(val) % 8)
        f.write(n_bytes.to_bytes(1))
        f.write(int(val, 2).to_bytes(n_bytes))
        f.write(int(last_byte, 2).to_bytes(1))
    f.close()


def save_huff_graph(huf_dic: dict, output_file: str, bin: bool):
    """save the huff graph in a file (binary file if the option is True)"""
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
                f.write(
                    len(key_utf8).to_bytes(1)
                )  # to decode we need to know how many bytes we use to encode the key
                f.write(key_utf8)  # encoding the key (letter)

                """to encode the value, we adopt the following scheme: 
                - a first byte to know how many bytes to encode the value
                - the binary code of the value
                - a last byte to know how many artificial 0s have been added in the first byte of the value (to fill the byte)
                ex for the val 1000011100 : 
                - 10 bits so we need 2 bytes, then we encode 2 : 00000010
                - then we encode the val in 2 bytes: 00000010 00011100
                - in the first byte we have 6 additional 0s so we encode 6 : 00000110
                -> 00000010 00000010 00011100 00000110"""
                how_many_bytes = len(val) // 8 + int(
                    bool(len(val) % 8)
                )  # number of bytes required
                last_byte = how_many_bits_more(len(val)).to_bytes(1)
                f.write(how_many_bytes.to_bytes(1))
                f.write(int(val, 2).to_bytes(how_many_bytes))
                f.write(last_byte)


def read_key_val(s: str):
    # first step : read the first byte, how many bytes to encode the key ?
    how_many_bytes = int(s[:8], 2)
    s = s[8:]

    # second step : read the letter which is encode in how_many_bytes bytes.
    letter_utf8 = s[: 8 * how_many_bytes]
    key = int(letter_utf8, 2).to_bytes(how_many_bytes).decode("utf-8")
    s = s[8 * how_many_bytes :]
    print(s)

    # third step : how many bytes required to encode the val ?
    how_many_bytes = int(s[:8], 2)
    s = s[8:]
    print(s)

    # fourth step : read the val
    val = s[: 8 * how_many_bytes]
    s = s[8 * how_many_bytes :]
    print(s)

    # fifth step : remove additional zeros
    how_many_zeros = int(s[:8], 2)
    val = val[how_many_zeros:]
    s = s[8:]
    return key, val, s


def read_huff_graph(huff_graph_file: str, bin: bool) -> dict:
    huff_dic = {}
    if not bin:
        pass
    else:
        with open(huff_graph_file, "rb") as f:
            content = f.read()
            f.close()
        encoded = ""
        for k in content:
            encoded += int_to_bytes(k)

        while (len(encoded)) > 0:
            key, val, encoded = read_key_val(encoded)
            huff_dic[key] = val
    return huff_dic
