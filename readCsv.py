import csv

data = []

f = open("test.csv", 'r')
reader = csv.reader(f)

for row in reader:
    data.extend(row)

print(len(data))

f.close
