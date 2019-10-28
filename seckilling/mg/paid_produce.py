# -*- coding: utf-8 -*-
# @Time    : 2019/10/25 22:20
# @Author  : CRJ
# @File    : paid_produce.py
# @Software: PyCharm
# @Python3.6
"""
    支付成功队列

"""
from conn import rabbitmq_conn
import json


def enter_paid_queue(order_info):
    """
        order_info包括userid、goodid、uuid等等



    :param order_info:
    :return:
    """
    user_id = order_info.get("user_id")
    order_id = order_info.get("order_id")
    goods_id = order_info.get("goods_id")
    if user_id is None or order_id is None or goods_id is None:
        return False

    channel = rabbitmq_conn.channel()

    exchange = 'paid.exchange'
    queue = 'paid.queue'
    routing_key = 'order.' + str(goods_id) + '.' + str(user_id)

    channel.exchange_declare(exchange=exchange,
                             exchange_type='topic',
                             durable=True)

    channel.queue_declare(queue=queue,
                          durable=True)

    channel.queue_bind(exchange=exchange,
                       queue=queue)

    # message = str(goods_id) + ',' + str(user_id) + ',' + str(order_id)
    message = json.dumps(order_info)

    channel.basic_publish(exchange=exchange,
                          routing_key=routing_key,
                          body=message)