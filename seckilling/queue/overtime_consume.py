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