dic = {"%": "100011110", "•": "01111011110011010001"}
# "|": "0111101111001101001"


def int_to_byteString(n: int) -> str:
    """convert integer into a string representing his byte writing"""
    seq = str(bin(n))[2:]
    l = len(seq)
    return (8 - l) * "0" + seq


def stringIntoByte(seq: str):
    n = len(seq)
    num = 0
    for k in range(n):
        num += int(seq[k]) * (2 ** (n - (k + 1)))
    return bytes(num.to_bytes(n // 8 + int(bool(n % 8))))


def write_char(char):
    b = bytes(char, "utf-8")
    return len(b).to_bytes(1), b


with open("test.bin", "wb") as f:
    for key, val in dic.items():
        f.write(write_char(key)[0])
        f.write(write_char(key)[1])
        n_bytes = len(val) // 8 + int(bool(len(val) % 8))  # number of bytes
        last_byte = int_to_byteString(len(val) % 8)
        f.write(n_bytes.to_bytes(1))
        f.write(stringIntoByte(val))
        f.write(stringIntoByte(last_byte))

print(len(bytes("•", "utf-8")))
