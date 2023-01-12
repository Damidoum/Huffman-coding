def int_to_bytes(n: int) -> str:
    """convert integer n into a STRING representing his byte writing"""
    seq = str(bin(n))[2:]  # [2:] because we remove 0b at the beginning
    l = len(seq)
    if l % 8 != 0:
        return (8 - l % 8) * "0" + seq
    else:
        return seq


def how_many_bits_more(l: int) -> int:
    additional_bits = l % 8
    if additional_bits == 0:
        return additional_bits
    else:
        return 8 - additional_bits


def bytes_to_int(s: str) -> int:
    """convert a STRING of 0 and 1 into int"""
    n = len(s)
    num = 0
    for k in range(n):
        num += int(s[k]) * (2 ** (n - (k + 1)))
    return num


def which_reader(bin):
    """if bin is true we read as 'rb', if not we read as 'r'"""
    if bin:
        return "rb"
    else:
        return "r"


def which_writer(bin):
    """if bin is true we write as 'wb', if not we read as 'w'"""
    if bin:
        return "wb"
    else:
        return "w"


def get_code_from_file(file: str) -> dict:
    """import the code of each letter from a text file"""
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


def read_key_val_huff_graph(s: str):
    # first step : read the first byte, how many bytes to encode the key ?
    how_many_bytes = int(s[:8], 2)
    s = s[8:]

    # second step : read the letter which is encode in how_many_bytes bytes.
    letter_utf8 = s[: 8 * how_many_bytes]
    key = int(letter_utf8, 2).to_bytes(how_many_bytes).decode("utf-8")
    s = s[8 * how_many_bytes :]

    # third step : how many bytes required to encode the val ?
    how_many_bytes = int(s[:8], 2)
    s = s[8:]

    # fourth step : read the val
    val = s[: 8 * how_many_bytes]
    s = s[8 * how_many_bytes :]

    # fifth step : remove additional zeros
    how_many_zeros = int(s[:8], 2)
    val = val[how_many_zeros:]
    s = s[8:]
    return key, val, s


def read_huff_graph(huff_graph_file: str, bin: bool) -> dict:
    huff_dic = {}
    if not bin:
        # text file
        with open(huff_graph_file, "r") as f:
            content = f.read()[1:-1].split(", ")
            for part in content:
                char = part.split(": ")
                key, val = char[0][1:-1], char[1][1:-1]
                huff_dic[key] = val
            f.close()
        # replacing \\n by \n
        if "\\n" in huff_dic.keys():
            huff_dic["\n"] = huff_dic["\\n"]
            del huff_dic["\\n"]
    else:
        with open(huff_graph_file, "rb") as f:
            content = f.read()
            f.close()
        encoded = ""
        for k in content:
            encoded += int_to_bytes(k)

        while (len(encoded)) > 0:
            key, val, encoded = read_key_val_huff_graph(encoded)
            huff_dic[key] = val
    return huff_dic


def decode(encoded, code):
    """decode a string of 0 and 1 with the huffman code"""
    decode = ""  # decoded file
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
    return decode
