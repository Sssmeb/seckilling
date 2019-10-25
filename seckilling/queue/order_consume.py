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