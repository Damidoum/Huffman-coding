def int_to_bytes(n: int) -> str:
    """convert integer n into a STRING representing his byte writing"""
    seq = str(bin(n))[2:]  # [2:] because we remove 0b at the beginning
    l = len(seq)
    if l % 8 != 0:
        return (8 - l % 8) * "0" + seq
    else:
        return seq


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
