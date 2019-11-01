# -*- coding: utf-8 -*-
# @Time    : 2019/10/25 22:03
# @Author  : CRJ
# @File    : order_produce.py
# @Software: PyCharm
# @Python3.6
"""
    订单生产者 （订单队列）

"""
from conn import rabbitmq_conn
import json

def enter_order_queue(order_info):
    """
        order_info包括userid、goodid、uuid等等


    :param order_info:
    :param timeout:
    :return:
    """
    user_id = order_info.get("user_id")
    order_id = order_info.get("order_id")
    goods_id = order_info.get("goods_id")
    if user_id is None or order_id is None or goods_id is None:
        return False

    channel = rabbitmq_conn.channel()

    exchange = 'order.exchange'
    queue = 'order.queue'
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
    print(333333333333333333)
    return True

enter_order_queue(order_info = {
            "goods_id": 1,
            "user_id": 2,
            "order_id": "asd"
        })