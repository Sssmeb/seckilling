# -*- coding: utf-8 -*-
# @Time    : 2019/10/25 22:15
# @Author  : CRJ
# @File    : overtime_produce.py
# @Software: PyCharm
# @Python3.6
"""
    超时队列

"""
from conn import rabbitmq_conn
import json

def enter_overtime_queue(order_info, timeout=15):
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

    # 延迟交换机
    delay_exchange = 'overtime.exchange.delay'
    # 延迟队列
    delay_queue = 'overtime.queue.delay'

    # 延迟交换机死信收容交换机
    exchange = 'overtime.exchange'
    # 延迟队列死信收容队列
    queue = 'overtime.queue'

    channel = rabbitmq_conn.channel()

    # 声明收容交换机
    channel.exchange_declare(exchange=exchange,
                             exchange_type='fanout',
                             durable=True)
    # 声明收容队列
    channel.queue_declare(queue=queue, durable=True)
    # 收容队列和收容交换机绑定
    channel.queue_bind(exchange=exchange, queue=queue)
    # 设置延迟队列参数
    arguments = {
        'x-message-ttl': 1000 * 60 * timeout,  # 延迟时间 （毫秒） 15min
        'x-dead-letter-exchange': exchange,  # 延迟结束后指向交换机（死信收容交换机）
        'x-dead-letter-routing-key': queue,  # 延迟结束后指向队列（死信收容队列）
    }

    # 申明面向生产者的交换机、和相应的队列
    channel.exchange_declare(exchange=delay_exchange,
                             exchange_type='fanout',
                             durable=True)
    channel.queue_declare(queue=delay_queue,
                          durable=True,
                          arguments=arguments)
    channel.queue_bind(exchange=delay_exchange, queue=delay_queue)

    # routing_key = 'overtime.' + str(goods_id) + '.' + str(user_id)
    # message = str(goods_id) + ',' + str(user_id) + ',' + str(order_id)
    message = json.dumps(order_info)

    channel.basic_publish(exchange=delay_exchange,
                          body=message,
                          routing_key="")

    return True