# -*- coding: utf-8 -*-
__author__ = "hulinjun"
import requests
from Mongomanage import Manangemongo
from bs4 import BeautifulSoup
URL = "http://sz.ganji.com/wu/"
BASE_URL = "http://sz.ganji.com"
HEADERS = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0"
}

def category_spider():
    """
    爬取深圳赶集网二手商品的品类
    :return:
    """
    rq = requests.get(url=URL,headers=HEADERS)
    soup = BeautifulSoup(rq.text,'lxml')
    categoryurl = [i.get('href') for i in soup.select('div.main-pop dl dt a')]
    whole_categoryurl = [BASE_URL + i for i in categoryurl]
    #保存到mongo
    mongo = Manangemongo('ganji','ershoushop')
    for each in whole_categoryurl:
        mongo.insert({
            "categorurl":each
        })

    print("保存成功")









if __name__ == '__main__':
    category_spider()