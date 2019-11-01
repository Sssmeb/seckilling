# -*- coding: utf-8 -*-
# @Time    : 2019/10/25 22:20
# @Author  : CRJ
# @File    : paid_consume.py
# @Software: PyCharm
# @Python3.6
"""
    监听支付队列

    有消息就读出
        1. 修改订单历史表（状态改为成功）
        2. 修改库存表 -1
        3. 写入redis 标识成功
"""
from utils import update_storage
import pika
from settings import RABBITMQ_HOST

def start_paid_consume(goods_id):
    rabbitmq_conn = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = rabbitmq_conn.channel()

    exchange = 'paid.exchange'
    queue = 'paid.queue'

    channel.exchange_declare(exchange=exchange,
                             exchange_type='topic',
                             durable=True)

    channel.queue_declare(queue=queue,
                          durable=True)

    channel.queue_bind(exchange=exchange,
                       queue=queue,
                       routing_key='order.' + str(goods_id) + '.' + '*')

    channel.basic_consume(on_message_callback=update_storage,
                          queue=queue,
                          auto_ack=False)

    channel.start_consuming()