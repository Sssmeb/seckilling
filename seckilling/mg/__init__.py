# -*- coding: utf-8 -*-
# @Time    : 2019/10/26 14:03
# @Author  : CRJ
# @File    : __init__.py
# @Software: PyCharm
# @Python3.6
from order_consume import start_order_consume
from overtime_consume import start_overtime_consume
from paid_consume import start_paid_consume


def start_consume(goods_id):
    start_order_consume(goods_id)
    start_overtime_consume(goods_id)
    start_paid_consume(goods_id)



if __name__ == '__main__':
    pass