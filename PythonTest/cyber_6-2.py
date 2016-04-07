import math


def main():
    a = 1528262114512379959787446361667336365541049710185448490827733939750117578606349583824805994668155766548948086204569455380471171904239315967452691
    key = 38108
    c, n = 0, 0
    i = math.floor(len(str(a)) / len(str(key)))
    # generate a key that is the same length as the input string:
    while n < i:
        c = 100000 * c + key
        n += 1
    # XOR the input string with the key:
    x = str(a ^ c)
    # print("XOR: ", x)
    y = ""
    while len(x) > 0:
        # Find printable characters and add them to the output string:
        if int(x[:2]) >= 32:
            y += chr(int(x[:2]))
            x = x[2:]
        else:
            y += chr(int(x[:3]))
            x = x[3:]

    print(y)

main()
