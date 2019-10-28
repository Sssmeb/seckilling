# -*- coding: utf-8 -*-
# @Time    : 2019/10/25 21:32
# @Author  : CRJ
# @File    : storage.py
# @Software: PyCharm
# @Python3.6
"""
    mysql库存相关接口

    表结构：
        1. 订单历史表
            - 订单id
            - user_id
            - goods_id
            - 提交时间
            - 状态 0表示未支付 1表示支付 -1表示超时

        2. 商品表
            - goods_id
            - 库存数量
"""
from conn import mysql_conn


def storage_insert_order(order_info):
    """
        订单队列的消费者 用来写入订单

    :param order_info:
    :return:
    """
    order_msg = order_info.split(',')
    if len(order_msg) == 3:
        goods_id, user_id, order_id = order_msg
        cur = mysql_conn.cursor()

        sql = "insert into order (goods_id, user_id, order_id) values (%s, %s, %s)"
        param = (goods_id, user_id, order_id)
        try:
            cur.execute(sql, param)
        except Exception as e:
            mysql_conn.rollback()
            print(e)
            return False
        finally:
            cur.close()
            mysql_conn.close()
        return True
    else:
        return False


def storage_update_order(order_info, flag=0):
    """
        支付队列的消费者 用来修改历史订单的状态

    :param order_info: message = str(goods_id) + ',' + str(user_id) + ',' + str(order_id)
    :return:
    """
    order_msg = order_info.split(',')
    if len(order_msg) == 3:
        goods_id, user_id, order_id = order_msg
        cur = mysql_conn.cursor()

        sql = "UPDATE order SET status=-1 where goods_id=%s and user_id=%s and order_id=%s"
        param = (goods_id, user_id, order_id)
        try:
            cur.execute(sql, param)
        except Exception as e:
            mysql_conn.rollback()
            print(e)
            return False
        finally:
            cur.close()
            mysql_conn.close()
        return True
    else:
        # 参数错误
        return False


def storage_update_storage(order_info):
    """
        支付队列的消费者 用来减库存

    :param order_info:
    :return:
    """
    order_msg = order_info.split(',')
    if len(order_msg) == 3:
        goods_id, user_id, order_id = order_msg
        cur = mysql_conn.cursor()

        sql = "UPDATE storage SET quantity=quantity-1 where id=%s"
        param = (goods_id)
        try:
            cur.execute(sql, param)
        except Exception as e:
            mysql_conn.rollback()
            print(e)
            return False
        finally:
            cur.close()
            mysql_conn.close()
        return True
    else:
        # 参数错误
        return False
