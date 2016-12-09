#!/usr/bin/python
# -*- coding:utf-8 -*-

import csv
from lxml import etree
import random
import requests
import sys
import time

## the shit encoding
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


## generate request headers from Mozilla Firefox 50.0
def headerGen(baseUrl):
    host = "www.dianping.com";
    referer = baseUrl;
    user_agent = "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0";
    accept = "text/html,text/javascript,application/json,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8";
    accept_language = "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3";
    accept_encoding = "gzip,deflate";
    connection = "keep-alive";
    headers = {'Host':host, 'Referer':referer, 'User-Agent':user_agent, 'Accept':accept, 'Accept-Languate':accept_language, 'Accept-Encoding':accept_encoding, 'Connection':connection};
    return headers;


## get html from webpage
def getHtml(url,param,header):
    page = "";
    time.sleep(random.randint(4,8));
    try:
        page = requests.get(url,params=param,headers=header);
    except requests.exceptions.Timeout:
        print("timeout...");
    except requests.exceptions.RequestException as e:
        print(e);
    html = etree.HTML(page.text);
    return html;


## get all shopId from type page
def getShopIDs(baseUrl):
    shopIDs = [];
    headers = headerGen(baseUrl);
    param = "";
    html = getHtml(baseUrl,param,headers);
    
    # get shop ids on this page
    shopListXpath = "//div[@class='shop-wrap']/div[@class='content']/div[@id='shop-all-list']/ul/li";
    shopList = html.xpath(shopListXpath);
    for shop in shopList:
        shopXpath = "./div[@class='pic']/a/@href";
        shopId = shop.xpath(shopXpath)[0].split('/')[-1];
        shopIDs.append(shopId);
    
    # how many pages of this type
    pageXpath = "//div[@class='shop-wrap']/div[@class='page']/a[@class='PageLink']/@title";
    pageNumList = html.xpath(pageXpath);
    pageNumMax = int(pageNumList[-1]);
    
    # get shop ids on other pages
    for pageNum in range(2,(pageNumMax+1)):
        url = baseUrl + "p" + str(pageNum);
        headers = headerGen(url);
        html = getHtml(url,param,headers);
        # get shop ids on this page
        shopListXpath = "//div[@class='shop-wrap']/div[@class='content']/div[@id='shop-all-list']/ul/li";
        shopList = html.xpath(shopListXpath);
        for shop in shopList:
            shopXpath = "./div[@class='pic']/a/@href";
            shopWord = shop.xpath(shopXpath)[0];
            shopId = shopWord.split('/')[-1];
            shopIDs.append(shopId);
    
    # return results
    return shopIDs;


## get information from this shop.
def getShopInfo(shopID):
    #shopID = "4668013";
    shopInfo = [];
    shopInfoLite = [];
    
    # get information from the first page
    baseUrl = "http://www.dianping.com/shop/" + shopID + "/review_all";
    headers = headerGen(baseUrl);
    params = {};
    html = getHtml(baseUrl,params,headers);
    # 
    dataIDs = html.xpath("//div[@class='comment-list']/ul/li/@data-id");
    
    # this shop may has no information
    if len(dataIDs) < 1:
        return [shopInfo,shopInfoLite];
    
    # get information from this page
    for dataId in dataIDs:
        userXpath = "//div[@class='comment-list']/ul/li[@data-id=" + dataId + "]/div[@class='pic']/a[@class='J_card']/@user-id";
        starXpath = "//div[@class='comment-list']/ul/li[@data-id=" + dataId + "]/div[@class='content']/div[@class='user-info']/span/@class";
        scoreXpath = "//div[@class='comment-list']/ul/li[@data-id=" + dataId + "]/div[@class='content']/div[@class='user-info']/div[@class='comment-rst']/span[@class='rst']/text()";
        commentXpath = "//div[@class='comment-list']/ul/li[@data-id=" + dataId + "]/div[@class='content']/div[@class='comment-txt']/div/text()";
        timestampXpath = "//div[@class='comment-list']/ul/li[@data-id=" + dataId + "]/div[@class='content']/div[@class='misc-info']/span[@class='time']/text()";
        userId = html.xpath(userXpath)[0];
        star = html.xpath(starXpath)[0][-2];
        scoreWordList = html.xpath(scoreXpath);
        score = [];
        if len(scoreWordList) < 3:
            score = ['0','0','0'];
        else:
            for i in [0,1,2]:
                score.append(scoreWordList[i][-1]);
        comment = html.xpath(commentXpath)[0].replace("\n","").replace(" ","");
        timestamp = html.xpath(timestampXpath)[0];
        # store them
        shopInfo.append([shopID,userId,star,score[0],score[1],score[2],timestamp,comment]);
        shopInfoLite.append([shopID,userId,star,score[0],score[1],score[2]]);
    
    # get information from other pages
    pageNumList = html.xpath("//a[@class='PageLink']/@data-pg");
    pageNumMax = int(pageNumList[-1]);
    for page in range(2,(pageNumMax+1)):
        params["pageno"] = page;
        html = getHtml(baseUrl,params,headers);
        # get information from this page
        dataIDs = html.xpath("//div[@class='comment-list']/ul/li/@data-id");
        for dataId in dataIDs:
            userXpath = "//div[@class='comment-list']/ul/li[@data-id=" + dataId + "]/div[@class='pic']/a/@user-id";
            starXpath = "//div[@class='comment-list']/ul/li[@data-id=" + dataId + "]/div[@class='content']/div[@class='user-info']/span/@class";
            scoreXpath = "//div[@class='comment-list']/ul/li[@data-id=" + dataId + "]/div[@class='content']/div[@class='user-info']/div[@class='comment-rst']/span[@class='rst']/text()";
            commentXpath = "//div[@class='comment-list']/ul/li[@data-id=" + dataId + "]/div[@class='content']/div[@class='comment-txt']/div/text()";
            timestampXpath = "//div[@class='comment-list']/ul/li[@data-id=" + dataId + "]/div[@class='content']/div[@class='misc-info']/span[@class='time']/text()"
            userId = html.xpath(userXpath)[0];
            star = html.xpath(starXpath)[0][-2];
            scoreWordList = html.xpath(scoreXpath);
            score = [];
            if len(scoreWordList) < 3:
                score = ['0','0','0'];
            else:
                for i in [0,1,2]:
                    score.append(scoreWordList[i][-1]);
            comment = html.xpath(commentXpath)[0].replace("\n","").replace(" ","");
            timestamp = html.xpath(timestampXpath)[0];
            # store them
            shopInfo.append([shopID,userId,star,score[0],score[1],score[2],timestamp,comment]);
            shopInfoLite.append([shopID,userId,star,score[0],score[1],score[2]]);
    
    # return result
    return [shopInfo,shopInfoLite];
    




