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