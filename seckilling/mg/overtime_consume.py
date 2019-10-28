# -*- coding: utf-8 -*-
# @Time    : 2019/10/25 22:14
# @Author  : CRJ
# @File    : overtime_consume.py
# @Software: PyCharm
# @Python3.6
"""
    监听超时队列

    只要存在消息 就读出
        1. 修改mysql订单历史
        2. 加入redis相关超时键
"""

from utils import overtime_order
import pika
from settings import RABBITMQ_HOST


def start_overtime_consume():
    rabbitmq_conn = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = rabbitmq_conn.channel()

    # 延迟交换机死信收容交换机
    exchange = 'overtime.exchange'
    # 延迟队列死信收容队列
    queue = 'overtime.queue'

    channel.exchange_declare(exchange=exchange,
                             exchange_type='fanout',
                             durable=True
                             )

    channel.queue_declare(queue=queue, durable=True)

    channel.basic_consume(on_message_callback=overtime_order,
                          queue=queue,
                          auto_ack=False)
    channel.start_consuming()



if __name__ == '__main__':
    pass