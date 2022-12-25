dic = {}
with open("code.coder", "r") as f:
    content = f.read().split(", ")[1:-1]
    for part in content:
        char = part.split(": ")
        key, val = char[0][1:-1], int(char[1][1:-1])
        dic[key] = val
    f.close()
print(dic)
