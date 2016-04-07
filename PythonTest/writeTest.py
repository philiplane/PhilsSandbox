__author__ = 'lane'
import json
myList = [1, 'simple', 'list']
# print(json.dumps(myList))
f = open('workfile', 'r+')
# f.flush()
lines = f.readlines()
f.seek(0)
f.truncate()
f.write('This is another line\n')
json.dump(myList, f)
for line in lines:
    print(line, end='')

print('\nfile size = ' + str(f.__sizeof__()))
f.close()

