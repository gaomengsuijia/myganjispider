# -*- coding: utf-8 -*-
__author__ = "hulinjun"
import threading
from Mongomanage import Manangemongo
from parsepage import Parsepage
def main():
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





if __name__ == '__main__':
    main()