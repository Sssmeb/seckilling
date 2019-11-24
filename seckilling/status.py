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
    改：
        除了order对应关系需要获取值 仍然用字典

        由于只需要判断是否存在 redis 中集合的底层实现是整数链表或哈希表
        所以此处用集合可以达到同样的效率，而不需要设置键值。

"""
from conn import redis_conn
from lock import release_lock,acquire_lock_with_timeout


def plus_counter(goods_id, storage=1000):
    """
        通过id 找到对应的键，加一
        返回 状态 （是否成功）
    :param goods_id:
    :param storage:
    :return:
    """
    # lock = acquire_lock_with_timeout(redis_conn, goods_id)
    # if lock:
    count = redis_conn.incr("counter:"+str(goods_id))
    # release_lock(redis_conn, goods_id, lock)
    if count > storage:
        return False

    return True

    # return False


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

    redis_conn.hset("order:"+str(goods_id), str(order_id), str(user_id))
    return True
    # else:
    #     return False


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
    if redis_conn.sismember("order:"+str(goods_id)+":"+"overtime", order_id):
        return -1
    else:
        return user_id == str(redis_conn.hget("order:" + str(goods_id), order_id), encoding="utf-8")


def enter_overtime(order_info):
    """
        在支付队列中，超时未支付（检查已成功支付的redis结构）
        写入redis中

    :param user_id:
    :param uuid:
    :return:
    """
    user_id = order_info.get("user_id")
    order_id = order_info.get("order_id")
    goods_id = order_info.get("goods_id")

    if _is_deal(order_info):
        return False
    else:
        redis_conn.sadd("order:"+str(goods_id)+":"+"overtime", order_id)
        return True


def _is_deal(order_info):
    """
        检查当前订单是否过期

    :param user_id:
    :param uuid:
    :return:
    """
    user_id = order_info.get("user_id")
    order_id = order_info.get("order_id")
    goods_id = order_info.get("goods_id")
    if redis_conn.sismember("order:"+str(goods_id)+":"+"deal", order_id):
        return True
    return False



def _is_overtime(order_info):
    """
        检查当前订单是否过期

    :param user_id:
    :param uuid:
    :return:
    """
    user_id = order_info.get("user_id")
    order_id = order_info.get("order_id")
    goods_id = order_info.get("goods_id")

    if redis_conn.sismember("order:"+str(goods_id)+":"+"overtime", order_id):
        return True
    return False


def paid_order(order_info):
    """
        标识该订单已支付完成

    :param user_id:
    :param uuid:
    :return:
    """
    # user_id = order_info.get("user_id")
    order_id = order_info.get("order_id")
    goods_id = order_info.get("goods_id")

    if _is_overtime(order_info):
        return False
    else:
        redis_conn.sadd("order:" + str(goods_id) + ":" + "deal", order_id)
        return True


if __name__ == '__main__':
    create_order(order_info = {
            "goods_id": 1,
            "user_id": 1,
            "order_id": "asd"
        })