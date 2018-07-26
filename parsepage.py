# -*- coding: utf-8 -*-
__author__ = "hulinjun"

import requests
from bs4 import BeautifulSoup
from Mongomanage import Manangemongo
from category import HEADERS
from requests.exceptions import ConnectionError
from config import COUNT
from poxyip import poxyip


man = Manangemongo('ganji','shopdetailurl')
poxy = None


class Parsepage(object):
    """
    解析网页
    """
    def __init__(self):
        pass


    def getsoup(self,url,count=0):
        """
        得到soup对象
        :param url:
        :return:
        """
        global poxy
        if count<=COUNT:
            try:
                if poxy:
                    proxies = {
                        "http": 'http://' + poxy,
                    }
                    req = requests.get(url=url,headers=HEADERS,proxies=proxies)
                else:
                    req = requests.get(url=url,headers=HEADERS)
                if req.status_code == 302:#爬虫被限制了，这个时候需要换个代理继续去访问
                    poxy = poxyip()
                    return self.getsoup(url)
                soup = BeautifulSoup(req.text,'lxml')
                return soup
            except ConnectionError as e:
                count += 1
                return self.getsoup(url)

        else:
            return None


    def get_shoplist(self,category,page=1):
        """
        得到每个商品分类的商品列表的商品详情url
        :return:
        """
        print("类目：{}开始爬取".format(category))
        for eachpage in range(page):#循环多页
            page_url = "{}/o{}".format(category,eachpage)
            soup = self.getsoup(page_url)
            if soup:
                all_shop = soup.select('tr.zzinfo')
                #去掉推广的商品
                temp = all_shop[:]#临时的列表，防止循环删除原列表时出现的坑啊
                for each in temp:
                    if each['class'] == ['zzinfo', 'jz']:
                        all_shop.remove(each)
                if all_shop:# 如果页码过大，没有数据时，页面只有推广的商品
                    for each in all_shop:
                        # shop_detail_url = soup.select('tr.zzinfo > td.t > a')
                        shop_detail_url = each.select('td.t > a')[0]
                        shop_detail_url = shop_detail_url.get('href')
                        shop_detail_url = shop_detail_url.split('?')[0]
                        man.insert({
                            "shopdetailurl":shop_detail_url
                        })
                else:
                    break

        print("类目：{}爬取完毕".format(category))




    def get_shopinfo(self,shop_detail_url):
        """
        获取每个商品详情页面的商品具体信息
        :param shop_detail_url:
        :return:
        """
        pass




if __name__ == '__main__':
    pa = Parsepage()
    pa.get_shoplist(2)