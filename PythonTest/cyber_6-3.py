__author__ = 'lane'

morse = {'.-': "A", '-...': "B", '-.-.': "C", '-..': "D", '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I',
         '.---': 'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
         '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y', '--..': 'Z', 'SP': ' '}

encoded = ['---', '..-.', '..-.', 'SP', '.--', '..', '-', '....', 'SP', '-', '....', '.', '..', '.-.', 'SP', '....',
           '.', '.-', '-..', '...']

os = ''
for x in encoded:
    os += morse[x]
print(os)
