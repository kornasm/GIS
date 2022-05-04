# script that group and count duplicate edges
# reult saved to a new file

from typing import Counter
import csv
from os.path import exists
import sys

def delete_comments(csvfile):
    for row in csvfile:
        raw = row.split('#')[0].strip()
        if raw:
            yield raw

currenturl = ''
filename = ''

if len(sys.argv) <= 1:
    print('Run this script with filename that contain edges to be counted')
    print('e.g. python3 CountEdges.py EkstraklasaEdges.csv')
    sys.exit()
else:
    filename = sys.argv[1]

if exists(filename) == False:
    sys.exit("File doesn't exist")

edges = []

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(delete_comments(csvfile), delimiter='+') # treat row as one record
    edges = list(csvreader)


for i in range(len(edges)):
    edges[i] = edges[i][0]

groupedEdges = Counter(edges)

outfile = '../data/Counted' + filename

with open(outfile, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['# id1', 'id2', 'weight'])
    for item in groupedEdges:
        ids = item.split(',')
        csvwriter.writerow([ids[0], ids[1], groupedEdges[item]])

print('Result saved to ' + outfile)