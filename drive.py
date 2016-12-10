#!/usr/bin/python
# -*- coding:utf-8 -*-

import csv
import os
import sys
import time
import dianping


## the shit encoding
reload(sys);
sys.setdefaultencoding('utf-8');


## get shop ids
typeId = 'g2926';
shopIDs = [];
# read shopIDs in
filename0 = "t_" + typeId + ".shoplist.csv";
csvfile0 = file(filename0,"r");
reader0 = csv.reader(csvfile0);

for row in reader0:
    shopIDs = shopIDs + row;

csvfile0.close();
# remove shops which have been searched.
filelist = os.listdir(".");

for filen in filelist:
    if (filen.startswith("t_" + typeId + "_s_") and filen.endswith(".lite.csv")):
        shopid = filen.replace("t_" + typeId + "_s_","").replace(".lite.csv","");
        while shopid in shopIDs:
            shopIDs.remove(shopid);

## get every thing.
timecount = 1;

for shopId in shopIDs:
    # just take a rest ^_^
    if timecount > 10:
        print("Let's take a rest for 5 minutes.");
        timecount = 1;
        time.sleep(300);
    
    # get the information of this shop
    [shopInfo,shopInfoLite] = dianping.getShopInfo(shopId);
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
    
    # timecount + 1
    timecount = timecount + 1;
