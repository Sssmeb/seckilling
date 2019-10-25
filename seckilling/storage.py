# -*- coding: utf-8 -*-
# @Time    : 2019/10/25 21:32
# @Author  : CRJ
# @File    : storage.py
# @Software: PyCharm
# @Python3.6
"""
    mysql库存相关接口

    表结构：
        1. 订单历史表
            - 订单id
            - user_id
            - goods_id
            - 提交时间
            - 状态 0表示未支付 1表示支付

        2. 商品表
            - goods_id
            - 库存数量
"""


def insert_order(order_info):
    """
        订单队列的消费者 用来写入订单

    :param order_info:
    :return:
    """
    pass


def update_order(order_info):
    """
        支付队列的消费者 用来修改历史订单的状态

    :param order_info:
    :return:
    """


def update_storage(order_info):
    """
        支付队列的消费者 用来减库存

    :param order_info:
    :return:
    """