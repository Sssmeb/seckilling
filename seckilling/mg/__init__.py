# -*- coding: utf-8 -*-
# @Time    : 2019/10/26 14:03
# @Author  : CRJ
# @File    : __init__.py
# @Software: PyCharm
# @Python3.6
from order_consume import start_order_consume
from overtime_consume import start_overtime_consume
from paid_consume import start_paid_consume
import threading

def start_consume(goods_id):
    t1 = threading.Thread(target=start_order_consume, args=(goods_id,))
    t2 = threading.Thread(target=start_overtime_consume)
    t3 = threading.Thread(target=start_paid_consume, args=(goods_id,))
    t1.start()
    t2.start()
    t3.start()



if __name__ == '__main__':
    pass