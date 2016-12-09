#!/usr/bin/python
# -*- coding:utf-8 -*-

import csv
import random
import sys
import time
import dianping


## the shit encoding
reload(sys);
sys.setdefaultencoding('utf-8');

## just for tourism in Beijing
baseUrl = "http://www.dianping.com/search/category/2/35/";
typeList = ['g33831','g2916','g2926','g2834','g5672','g27852','g20038'];


## get information of shops in type 2.

typeId = typeList[2];
url = baseUrl + typeId;
shopIDs = getShopIDs(url);
# store it
filename0 = "t_" + typeId + ".shoplist.csv";
csvfile0 = file(filename0,"wb");
writer0 = csv.writer(csvfile0);
writer0.writerows([typeId] + shopIDs);
csvfile0.close();

# get every thing.
shopInfoTotal = [];
shopInfoTotalLite = [];
for shopId in shopIDs:
    # get the information of this shop
    time.sleep(random.randint(8,12));
    [shopInfo,shopInfoLite] = getShopInfo(shopId);
    if len(shopInfo) < 1:
        message = "shop " + shopId + " has no comments yet.";
        print(message);
    else:
        filename1 = "t_" + typeId + "_s_" + shopId + ".csv";
        filename2 = "t_" + typeId + "_s_" + shopId + ".lite.csv";
        csvfile1 = file(filename1,"wb");
        csvfile2 = file(filename2,"wb");
        writer1 = csv.writer(csvfile1);
        writer2 = csv.writer(csvfile2);
        writer1.writerows(shopInfo);
        writer2.writerows(shopInfoLite);
        csvfile1.close();
        csvfile2.close();
        message = "shop " + shopId + " has been saved.";
        print(message);
        shopInfoTotal = shopInfoTotal + shopInfo;
        shopInfoTotalLite = shopInfoTotalLite + shopInfoLite;
filename3 = "t_" + typeId + ".shopinfo.csv";
csvfile3 = file(filename3,"wb");
writer3 = csv.writer(csvfile3);
writer3.writerows(shopInfoTotal);
csvfile3.close();
filename4 = "t_" + typeId + ".shopinfo.lite.csv";
csvfile4 = file(filename4,"wb");
writer4 = csv.writer(csvfile4);
writer4.writerows(shopInfoTotalLite);
csvfile4.close();


