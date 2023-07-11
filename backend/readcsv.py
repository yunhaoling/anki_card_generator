import csv

from data import FrontBackPair


def process_csv(csvfile):
    spamreader=csv.reader(csvfile,delimiter=',')
    res=[]
    for row in spamreader:
        if len(row) == 1:
            res.append(FrontBackPair(row[0],None))
        else:
            res.append(FrontBackPair(row[0],row[1]))
    return res


def read_and_process_csv_file(csvfile_path):
    with open(csvfile_path, newline='') as csvfile:
        process_csv(csvfile)
