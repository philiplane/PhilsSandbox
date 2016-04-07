__author__ = 'lane'

x = ["4c", "62", "68", "27", "65", "72", "20", "7a", "6e", "71",
     "2e", "22", "20", "22", "55", "62", "6a", "20", "71", "62",
     "20", "6c", "62", "68", "20", "78", "61", "62", "6a", "20",
     "56", "27", "7a", "20", "7a", "6e", "71", "3f", "22", "20",
     "66", "6e", "76", "71", "20", "4e", "79", "76", "70", "72",
     "2e", "20", "22", "4c", "62", "68", "20", "7a", "68", "66",
     "67", "20", "6f", "72", "2c", "22", "20", "66", "6e", "76",
     "71", "20", "67", "75", "72", "20", "50", "6e", "67", "2c",
     "20", "22", "62", "65", "20", "6c", "62", "68", "20", "6a",
     "62", "68", "79", "71", "61", "27", "67", "20", "75", "6e",
     "69", "72", "20", "70", "62", "7a", "72", "20", "75", "72",
     "65", "72", "2e"]
s = ""
UPPER_OFFSET = 65
LOWER_OFFSET = 97
KEY = 13

for i in x:
    # convert the input data to ASCII:
    ch = chr(int("0x" + i, 0))
    # Decode the alphanumeric characters using a Caesar cipher decoder and add them to the output string:
    if ch.isalpha():
        a = ord(ch)
        if ch.isupper():
            a = ((a - UPPER_OFFSET) + KEY) % 26 + UPPER_OFFSET
        else:
            a = ((a - LOWER_OFFSET) + KEY) % 26 + LOWER_OFFSET
        s += chr(a)
    else:
        s += ch
print(s)
