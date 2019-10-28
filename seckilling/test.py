# -*- coding: utf-8 -*-
# @Time    : 2019/10/28 21:35
# @Author  : CRJ
# @File    : test.py
# @Software: PyCharm
# @Python3.6
import time
def test():
    for i in range(5):
        print(i)
        yield
        time.sleep(i)

if __name__ == '__main__':
    test()





# import uuid
#
# a = uuid.uuid1()
# print(a)
# print(type(a))
# print(type(str(a)))
