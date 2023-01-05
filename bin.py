# With binary file
import random
import operator

# create random bytes
def randomBytes(size):
    return [random.randrange(0, 255) for _ in range(size)]


def displayBytes(bytes):
    print("-" * 20)
    for index, item in enumerate(bytes, start=1):
        print(f"{index} = {item} ({hex(item)})")
    print("-" * 20)


with open("info.bin", "wb") as file:
    a = 0b0001
    file.write(bytes.fromhex("0xff"))
    file.close()
