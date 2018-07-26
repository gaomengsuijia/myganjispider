# -*- coding: utf-8 -*-
__author__ = "hulinjun"
import requests
from config import POXYIPURL,COUNT_IP
from requests.exceptions import ConnectionError
import json
def poxyip(count=1):
    """
     代理ip获取
    """
    # global COUNT_IP
    if count<=COUNT_IP:
        try:
            req = requests.get(url=POXYIPURL)
            return json.loads(req.text)['ip']
        except ConnectionError:
            count -= 1
            poxyip()
    else:
        return None

if __name__ == '__main__':
    poxyip()