"""
    请求相关接口

"""

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


# 抢购接口
@app.route('/purchase')
def purchase(user_id):
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
    pass


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
    app.run()
