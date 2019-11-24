# seckilling

用python+redis+rabbitmq搭建一个简单的秒杀系统。由于是从项目中抽离出来的一个部分，所以省略了其他业务功能接口，只包含秒杀系统相关程序。

具体架构分析见博客：https://www.jianshu.com/p/ef6d25397f04



## 基础流程、架构

### 基础预设

0. mysql中存储商品信息、订单信息

1. redis存入商品信息、设置计数器、存储成功订单的数据结构等
2. rabbitmq创建队列
   - 订单队列
   - 延迟队列（场景如：订单必须在15分钟内支付）
   - 成交队列

### 基础架构

**注：服务异步拆分，减少耦合，加快响应。（rabbitmq）**

避免同步的执行，如：请求→订单→支付→修改库存→结束返回，这种模型在高并发场景下，阻塞多，响应慢，服务器压力大，明显的不可取的。

这里实现的架构是： 1. 请求→返回  	2. 支付→返回	 3. 修改库存

1. 用户提交订单

   - 通过redis计数器筛选

   - 成功则返回标识，然后入订单队列 + 超时队列
     - 标识与用户信息写入redis，用于后续验证支付
     - 订单队列，mysql监听，写入mysql的订单历史表
     - 超时订单队列有计时功能，一定时间内未支付，订单失效，抢购失败。写入redis（标志失败）
   - 失败直接返回
   - 订单服务结束

2. 用户支付订单

   - 验证订单以及检查是否已超时（是否已在redis相关结构内）

   - 成功支付则入支付队列
     - mysql监听这个队列，执行库存同步操作。
     - 写入redis
   - 失败或超时直接返回
   - 支付服务结束

## 注

### 计数器为什么不需要分布式锁

起初版本在计数器+1时使用了分布式锁，是想避免并发情况下出现数据不安全的情况。

```python
def plus_counter(goods_id, storage=1000):
    lock = acquire_lock_with_timeout(redis_conn, goods_id)
    if lock:
        count = redis_conn.incr("counter:"+str(goods_id))
        release_lock(redis_conn, goods_id, lock)
        if count > storage:
            return False

        return True

    return False
```

但是后续再整理代码，仔细思考得出结论：此处不需要分布式锁。原因是：

1. redis提供的incr命令是原子性的
2. redis是单线程模型
3. 此处应用程序不需要获取数据，经过逻辑判断以后再写入数据库。仅是单一语句，获取结果。

如果我们的场景是：

```python
now = redis.get(xxx)
if now==yyy:
	new = 123
elif now ==www:
	new = 456

redis.set(xxx, new)
```

那么由于在我们做逻辑判断是过程中，其他客户端可能会修改xxx的值，导致错误。在这种场景下，从get到set之间就需要加锁，保证这期间数据不会受其他客户端的影响。

但是由于我们计数器应用仅需要执行incr语句，获取返回值。而redis中incr指令是原子性的，且是单线程通过队列串行执行的，所以能保证incr在执行期间不会受到其他线程的影响。所以不需要加锁。





