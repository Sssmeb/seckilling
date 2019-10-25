# -*- coding: utf-8 -*-
# @Time    : 2019/10/25 22:03
# @Author  : CRJ
# @File    : order_produce.py
# @Software: PyCharm
# @Python3.6
"""
    订单生产者 （订单队列）

"""


def enter_order_queue(order_info, timeout=30):
    """
        order_info包括userid、goodid、uuid等等
        订单超时时间



    :param order_info:
    :param timeout:
    :return:
    """