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


def encode_file(file: str, code: str, output: str):
    dic = get_code_from_file(code)
    output_file = open(output, "w")
    with open(file, "r") as f:
        for line in f.readlines():
            for letter in line[:-1]:
                output_file.write(dic[letter])
            output_file.write(dic["\n"])
        f.close()
    output_file.close()


dic = get_code_from_file("code.coder")
print(dic)
encode_file("../python-eval-groupe1/sample-01.txt", "code.coder", "output.txt")
