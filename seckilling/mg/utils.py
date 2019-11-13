# -*- coding: utf-8 -*-
# @Time    : 2019/10/28 14:05
# @Author  : CRJ
# @File    : utils.py
# @Software: PyCharm
# @Python3.6
from status import enter_overtime, paid_order
from storage import storage_update_order, storage_insert_order, storage_update_storage
import json
import time


def overtime_order(ch, method, properties, body):
    """
    :param ch:
    :param method:
    :param properties:
    :param body: message = str(goods_id) + ',' + str(user_id) + ',' + str(order_id)
    :return:
    """
    # 如果是超时 则修改数据库中状态。否则是已完成的订单
    body = str(body, encoding="utf-8")
    body = json.loads(body)
    if enter_overtime(body):
        storage_update_order(body, -1)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def insert_order(ch, method, properties, body):
    body = json.loads(body)
    if storage_insert_order(body):
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        ch.basic_nack(delivery_tag=method.delivery_tag)


def update_storage(ch, method, properties, body):
    body = json.loads(body)
    if storage_update_storage(body) and storage_update_order(body, 1) and paid_order(body):
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        ch.basic_nack(delivery_tag=method.delivery_tag)

