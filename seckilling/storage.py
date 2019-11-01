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
from conn import mysql_pool
import pymysql


def storage_insert_order(order_info):
    """
        订单队列的消费者 用来写入订单

    :param order_info:
    :return:
    """
    # mysql_conn = mysql_pool.connection()
    mysql_conn = pymysql.connect(host='localhost', user='root', passwd='root', db='seckilling', port=3306)
    cur = mysql_conn.cursor()

    user_id = order_info.get("user_id")
    order_id = order_info.get("order_id")
    goods_id = order_info.get("goods_id")

    sql = "insert into order_history (goods_id, user_id, order_id) values (%s, %s, %s)"
    param = (goods_id, user_id, order_id)
    try:
        cur.execute(sql, param)
        mysql_conn.commit()
        return True
    except Exception as e:
        mysql_conn.rollback()
        print(e)
        return False
    finally:
        cur.close()
        mysql_conn.close()



def storage_update_order(order_info, flag=0):
    """
        支付队列的消费者 用来修改历史订单的状态

    :param order_info: message = str(goods_id) + ',' + str(user_id) + ',' + str(order_id)
    :return:
    """
    mysql_conn = mysql_pool.connection()
    cur = mysql_conn.cursor()

    user_id = order_info.get("user_id")
    order_id = order_info.get("order_id")
    goods_id = order_info.get("goods_id")

    sql = "UPDATE order_history SET status=%s where goods_id=%s and user_id=%s and order_id=%s"
    param = (str(flag), goods_id, user_id, order_id)
    try:
        cur.execute(sql, param)
        mysql_conn.commit()
        return True
    except Exception as e:
        mysql_conn.rollback()
        print(e)
        return False
    finally:
        cur.close()
        mysql_conn.close()



def storage_update_storage(order_info):
    """
        支付队列的消费者 用来减库存

    :param order_info:
    :return:
    """
    mysql_conn = mysql_pool.connection()
    cur = mysql_conn.cursor()

    # user_id = order_msg.get("user_id")
    # order_id = order_msg.get("order_id")
    goods_id = order_info.get("goods_id")

    sql = "UPDATE storage SET quantity=quantity-1 where id=%s"
    param = (goods_id)
    try:
        cur.execute(sql, param)
        mysql_conn.commit()
        return True
    except Exception as e:
        mysql_conn.rollback()
        print(e)
        return False
    finally:
        cur.close()
        mysql_conn.close()


if __name__ == '__main__':
    storage_insert_order(order_info = {
            "goods_id": 1,
            "user_id": 2,
            "order_id": "asd"
        })
