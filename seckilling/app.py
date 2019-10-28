"""
    请求相关接口

"""

from flask import Flask, jsonify, request
from status import *
from mg.order_produce import enter_order_queue
from mg.overtime_produce import enter_overtime_queue
import uuid
from mg import start_consume


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


# 抢购接口
@app.route('/purchase')
def purchase():
    # user_id, goods_id
    user_id = request.args.get("user_id")
    goods_id = request.args.get("goods_id")

    """
        0. 由于省略了用户相关业务，所以直接传值代表用户id，仅做测试。

        流程：
        1. redis计数器判断
            - 计数器设置为库存数量
            - 当超过计数器时，直接返回失败。
        2. 通过计数器的订单获得一个唯一标识
            - 将用户-标识 写入redis
            - 写入订单队列 + 超时队列

    :return: 返回状态 + 标识
    """
    res = {
        "status": False,
        "msg": ""
    }

    flag = plus_counter(goods_id)
    # 成功申请
    if flag:
        # 生成唯一的订单号
        order_id = uuid.uuid1()
        order_info = {
            "goods_id": goods_id,
            "user_id": user_id,
            "order_id": order_id
        }
        try:
            create_order(order_info)

            enter_order_queue(order_info)

            enter_overtime_queue(order_info)
        except Exception as e:
            print("log: ", e)
            res["status"] = False
            res["msg"] = "抢购出错，请重试." + str(e)
            return jsonify(res), 202

    # 计数器超出，直接返回
    else:
        res["status"] = False
        res["msg"] = "商品已售罄"
        return jsonify(res), 200

@app.route('/pay')
def pay(user_id, order_id):
    """
        1. 检查
            - 通过redis检查用户和订单是否对应
            - 通过redis检查订单是否已过期
        2. 支付成功
            - 写入成功队列 （由mysql服务监听）
            - 写入redis （标志为成功）

    :param user_id:
    :param order_id:
    :return:
    """
    pass


if __name__ == '__main__':
    # start_consume(1)
    app.run()
