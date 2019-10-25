# -*- coding: utf-8 -*-
# @Time    : 2019/10/25 21:33
# @Author  : CRJ
# @File    : status.py
# @Software: PyCharm
# @Python3.6
"""
    redis临时状态存储接口

    键：
        1. 计数器 str
        2. order对应关系、超时队列、成功队列 —— 字典 用户-uuid

"""


# def counter(goods_id, goods_storage):
#     """
#         通过id和库存量 生成一个计数器
#
#     :param goods_id:
#     :param goods_storage:
#     :return:
#     """
#     pass


def plus_counter(goods_id, storage=1000):
    """
        通过id 找到对应的键，加一
        返回 状态 （是否成功）
    :param goods_id:
    :param storage:
    :return:
    """
    pass


def create_order(user_id, uuid):
    """
        建立user和uuid的对应关系 用于后续支付验证

    :param user_id:
    :param uuid:
    :return:
    """
    pass


def check_order(user_id, uuid):
    """
        支付时用于验证
        还要检查订单是否过期
    :param user_id:
    :param uuid:
    :return:
    """
    pass


def overtime(user_id, uuid):
    """
        在支付队列中，超时未支付（检查已成功支付的redis结构）
        写入redis中

    :param user_id:
    :param uuid:
    :return:
    """
    pass


def check_time(user_id, uuid):
    """
        检查当前订单是否过期

    :param user_id:
    :param uuid:
    :return:
    """


def paid_order(user_id, uuid):
    """
        标识该订单已支付完成

    :param user_id:
    :param uuid:
    :return:
    """