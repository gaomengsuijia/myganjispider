# -*- coding: utf-8 -*-
__author__ = "hulinjun"
import requests
from bs4 import BeautifulSoup
from Mongomanage import Manangemongo
from category import HEADERS
from requests.exceptions import ConnectionError
from config import COUNT
from poxyip import poxyip
import re

man = Manangemongo('ganji','shopdetailurl')
mangoodinfo = Manangemongo('ganji','goodinfo')
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
                if req.status_code == 404:#商品url不可用
                    return None
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



    def saveto_mongo(self,data):
        """
        将商品详情数据保存到mongo中
        :param data:
        :return:
        """
        mangoodinfo.insert(data)


    def get_shopinfo(self,shop_detail_url):
        """
        获取每个商品详情页面的商品具体信息
        :param shop_detail_url:
        :return:
        """
        soup = self.getsoup(shop_detail_url)
        if soup:
            soldout_btn = soup.select('.soldout_btn')
            if soldout_btn:#商品下架
                return
            #提取数字
            parten = re.compile(r'\d+')
            good_title = soup.select('.info_titile')[0].get_text()
            price_now = soup.select('.price_now > i')[0].get_text()
            price_ori = soup.select('.price_ori')
            #如果没有原价就默认为''
            price_ori = parten.findall(price_ori[0].get_text())[0] if price_ori else ''
            address = soup.select('.palce_li > span > i')[0].get_text()
            seller = soup.select('.personal_name')[0].get_text()
            #如果没有浏览量就默认为''
            look_time = soup.select('.look_time')
            look_time = parten.findall(look_time[0].get_text())[0] if look_time else ''
            want_person = soup.select('.want_person')[0].get_text()
            want_person = parten.findall(want_person)[0]
            data = {
                "good_title":good_title,
                "price_now":price_now,
                "price_ori":price_ori,
                "address":address,
                "seller":seller,
                "look_time":look_time,
                "want_person":want_person
            }
            self.saveto_mongo(data)


if __name__ == '__main__':
    pa = Parsepage()
    # pa.get_shopinfo("http://zhuanzhuan.ganji.com/detail/1022661804963479566z.shtml")
    x = pa.get_shopinfo("http://zhuanzhuan.ganji.com/detail/1021954963855392786z.shtml")