def get_code_from_file(file: str) -> dict:
    dic = {}
    with open(file, "r") as f:
        content = f.read()[1:-1].split(", ")
        for part in content:
            char = part.split(": ")
            key, val = char[0][1:-1], char[1][1:-1]
            dic[key] = val
        f.close()

    if "\\n" in dic.keys():
        dic["\n"] = dic["\\n"]
        del dic["\\n"]
    return dic


def encode_file(file: str, code: str, output: str) -> None:
    dic = get_code_from_file(code)
    output_file = open(output, "w")
    with open(file, "r") as f:
        for line in f.readlines():
            for letter in line[:-1]:
                output_file.write(dic[letter])
            output_file.write(dic["\n"])
        f.close()
    output_file.close()


def decode_file(encode_file: str, code: dict, output_file: str) -> None :
    with open(encode_file, "r") as f:
        encode = f.read()
        f.close()

    out = ""

    while len(encode) > 0:
        key = ""
        count = 1
        possibilities = dic.keys()
        while len(possibilities) > 1:
            for char in encode:
                key += char
                possibilities = [x for x in possibilities if x[:count] == key]
                count += 1
                if len(possibilities) == 1:
                    break
        encode = encode[len(key) :]
        out += dic[key]
    
    with open(output_file, "w") as f : 
        f.write(out)
        f.close()


dic = {v: k for k, v in get_code_from_file("english.coder").items()}
encode_file("data/sample-01.txt", "english.coder", "sample-01-encode.txt")
decode_file("sample-01-encode.txt",dic, "sample-01-decode.txt")