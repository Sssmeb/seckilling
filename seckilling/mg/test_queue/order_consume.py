# -*- coding: utf-8 -*-
# @Time    : 2019/10/25 22:08
# @Author  : CRJ
# @File    : order_consume.py
# @Software: PyCharm
# @Python3.6
"""
    监听订单队列

    只要存在消息 就读出， 然后写入mysql订单历史
    此时交易未成交 所以交易状态是未完成
"""
import pika
from settings import RABBITMQ_HOST
from utils import insert_order
import time

rabbitmq_conn = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = rabbitmq_conn.channel()

exchange = 'order.exchange'
queue = 'order.queue'

channel.exchange_declare(exchange=exchange,
                         exchange_type='topic',
                         durable=True)

channel.queue_declare(queue=queue,
                      durable=True)

channel.queue_bind(exchange=exchange,
                   queue=queue,
                   routing_key='order.' + str(1) + '.' + '*')

channel.basic_consume(on_message_callback=insert_order,
                      queue=queue,
                      auto_ack=False)
channel.start_consuming()

print(1111111111111111)
