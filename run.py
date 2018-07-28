# -*- coding: utf-8 -*-
__author__ = "hulinjun"

import gevent
from gevent import monkey
monkey.patch_all()
import threading
from Mongomanage import Manangemongo
from parsepage import Parsepage
from config import RUN_GOODINFO,RUN_GOODDETAIL
import multiprocessing
import time

def main():
    # 抓取商品的detail页面url
    if RUN_GOODDETAIL:

        mongo = Manangemongo('ganji', 'ershoushop')
        all_category = mongo.find()
        par = Parsepage()
        td = []
        for each in all_category:
            ts = threading.Thread(target=par.get_shoplist,args=(each['categorurl'],500))
            td.append(ts)

        for each in td:
            each.start()
            each.join()

    # 抓取商品详情的info信息
    if RUN_GOODINFO:
        #从mongo中拿到url
        man = Manangemongo('ganji', 'shopdetailurl')
        all = man.find()
        par = Parsepage()
        print("开始爬取.........")
        #几十万条的数据，用携程会报memoryerror，怎么搞啊
        # u = [gevent.spawn(par.get_shopinfo,i['shopdetailurl']) for i in all]
        # gevent.joinall(u)
        for each in all:
            par.get_shopinfo(each['shopdetailurl'])
        print("爬取结束........")


def print_num():
    mans = Manangemongo('ganji', 'goodinfo')
    while True:
        time.sleep(60)
        num = mans.find().count()
        print("已插入数据：%s条" % (num,))


def shijian():
    start_time = time.time()
    while True:
        time.sleep(600)
        ecl_time = (time.time() - start_time) / 1000 / 60 / 60
        print("已消耗时间:{}".format(ecl_time))




if __name__ == '__main__':
    pros1 = multiprocessing.Process(target=main)
    pros2 = multiprocessing.Process(target=print_num)
    pros3 = multiprocessing.Process(target=shijian)
    pros1.start()
    pros2.start()
    pros3.start()