# -*- coding: utf-8 -*-
# @Time    : 2019/10/25 21:33
# @Author  : CRJ
# @File    : status.py
# @Software: PyCharm
# @Python3.6
"""
    redis临时状态存储接口

    键：
        1. 计数器 str
        2. order对应关系、超时队列、成功队列 —— 字典 uuid-orderinfo

        "order:"+str(goods_id)
        "order:"+str(goods_id)+":"+"overtime"
        "order:"+str(goods_id)+":"+"deal"

"""
from conn import redis_conn

# def counter(goods_id, goods_storage):
#     """
#         通过id和库存量 生成一个计数器
#
#     :param goods_id:
#     :param goods_storage:
#     :return:
#     """
#     pass


def plus_counter(goods_id, storage=1000):
    """
        通过id 找到对应的键，加一
        返回 状态 （是否成功）
    :param goods_id:
    :param storage:
    :return:
    """
    count = redis_conn.incr("counter:"+str(goods_id))
    if count > storage:
        return False
    return True


def create_order(order_info):
    """
        建立user和uuid的对应关系 用于后续支付验证

    :param user_id:
    :param uuid:
    :return:
    """
    user_id = order_info.get("user_id")
    order_id = order_info.get("order_id")
    goods_id = order_info.get("goods_id")
    if user_id is None or order_id is None or goods_id is None:
        return False

    order_map = {
        str(user_id): order_id
    }
    redis_conn.hmset("order:"+str(goods_id), order_map)
    return True


"""
"order:"+str(goods_id)
"order:"+str(goods_id)+":"+"overtime"
"order:"+str(goods_id)+":"+"deal"
"""


def check_order(order_info):
    """
        支付时用于验证
        还要检查订单是否过期
    :param user_id:
    :param uuid:
    :return:
    """
    user_id = order_info.get("user_id")
    order_id = order_info.get("order_id")
    goods_id = order_info.get("goods_id")

    # 如果已存在超时队列
    if redis_conn.hexists("order:"+str(goods_id)+":"+"overtime", order_id):
        return False
    else:
        return user_id == redis_conn.hget("order:"+str(goods_id), order_id)


def enter_overtime(order_info):
    """
        在支付队列中，超时未支付（检查已成功支付的redis结构）
        写入redis中

    :param user_id:
    :param uuid:
    :return:
    """
    # user_id = order_info.get("user_id")
    order_id = order_info.get("order_id")
    goods_id = order_info.get("goods_id")

    if _is_deal(order_info):
        return False
    else:
        redis_conn.hset("order:"+str(goods_id)+":"+"overtime", order_id)
        return True


def _is_deal(order_info):
    """
        检查当前订单是否过期

    :param user_id:
    :param uuid:
    :return:
    """
    order_id = order_info.get("order_id")
    goods_id = order_info.get("goods_id")
    if redis_conn.hexists("order:"+str(goods_id)+":"+"deal", order_id):
        return True
    return False


def _is_overtime(order_info):
    """
        检查当前订单是否过期

    :param user_id:
    :param uuid:
    :return:
    """
    order_id = order_info.get("order_id")
    goods_id = order_info.get("goods_id")
    if redis_conn.hexists("order:"+str(goods_id)+":"+"overtime", order_id):
        return True
    return False


def paid_order(order_info):
    """
        标识该订单已支付完成

    :param user_id:
    :param uuid:
    :return:
    """
    order_id = order_info.get("order_id")
    goods_id = order_info.get("goods_id")

    if _is_overtime(order_info):
        return False
    else:
        redis_conn.hset("order:" + str(goods_id) + ":" + "deal", order_id)
        return True

if __name__ == '__main__':
    create_order(order_info = {
            "goods_id": 1,
            "user_id": 1,
            "order_id": "asd"
        })