#!/usr/bin/python
# -*- coding:utf-8 -*-

from lxml import etree
import random
import requests
import sys
import time

## the shit encoding
reload(sys);
sys.setdefaultencoding('utf-8');


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
    




