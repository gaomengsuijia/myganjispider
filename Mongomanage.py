# -*- coding: utf-8 -*-
__author__ = "hulinjun"
from pymongo import MongoClient

MONGOSETTING = {
    "ip":"localhost",
    "port":27017
}


class Manangemongo(object):
    """
    操作mongo
    """
    def __init__(self,db,collection):
        self.mongoclint = MongoClient(MONGOSETTING['ip'],MONGOSETTING['port'])
        self.db = self.mongoclint[db]
        self.collection = self.db[collection]


    def insert(self,dic):
        """
        insert data
        :param dic:
        :return:
        """
        try:
            self.collection.insert(dic)
        except Exception:
            raise Exception("保存到mongo失败")



    def update(self,old_dic,new_dic):
        """
        update data
        :param old_dic:
        :param new_dic:
        :return:
        """
        self.collection.update(old_dic,new_dic)

    def delete(self,dic):
        """
        delete
        :param dic:
        :return:
        """
        self.collection.remove(dic)


    def find(self,dic=None):
        """
        find data
        :param dic:
        :return:
        """
        if dic:
            return self.collection.find(dic)
        else:
            return self.collection.find()




if __name__ == '__main__':
    man = Manangemongo('ganji', 'shopdetailurl')
    man1 = Manangemongo('ganji', 'goodinfo')
    all_ship = man.find().count()
    goodinfo = man1.find().count()
    print(all_ship)
    print(goodinfo)