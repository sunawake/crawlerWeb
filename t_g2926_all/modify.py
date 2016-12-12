#!/usr/bin/python
# -*- coding:utf-8 -*-

import csv
import os

# read filelist
filelist = os.listdir("ori");

for filee in filelist:
    result = [];
    filename0 = os.getcwd() + os.sep + "ori" + os.sep + filee;
    csvfile0 = file(filename0,"r");
    reader0 = csv.reader(csvfile0);
    for row in reader0:
        result.append([row[0],row[1],row[4],row[5],row[6],row[7],row[2],row[3]]);
    csvfile0.close();
    filename1 = filee;
    csvfile1 = file(filename1,"wb");
    writer1 = csv.writer(csvfile1);
    writer1.writerows(result);
    csvfile1.close();

os.system("rm -rf ori");
