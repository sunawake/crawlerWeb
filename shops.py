#!/usr/bin/python
# -*- coding:utf-8 -*-

import csv
import dianping

## just for tourism in Beijing
baseUrl = "http://www.dianping.com/search/category/2/35/";
typeList = ['g33831','g2916','g2926','g2834','g5672','g27852','g20038'];


## get information of shops in every type.

for typeId in typeList:
    url = baseUrl + typeId;
    shopIDs = dianping.getShopIDs(url);
    # store it
    filename0 = "t_" + typeId + ".shoplist.csv";
    csvfile0 = file(filename0,"wb");
    writer0 = csv.writer(csvfile0);
    writer0.writerows([shopIDs]);
    csvfile0.close();
    message = "type " + typeId + " has been searched.";
    print(message);
