with open('foo.txt', 'r+') as myFile:
    data = myFile.readlines()

for x in data:
    if "Status" in x:
        print x[8:]
