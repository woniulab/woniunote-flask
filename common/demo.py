# from PIL import Image   # 导入pillow库的Image模块
# import os
#
# # 定义原始图片路径
# source = 'D:/source.jpg'
# # 以KB为单位获取图片大小
# size = int(os.path.getsize(source) / 1024)
# print("原始图片大小为：%d KB" % size)
#
# # 调整图片大小为1000的宽度
# im = Image.open(source)
# width, height = im.size
# print(width, height)
# # if width > 1000:
# #     # 等比例缩放
# #     height = int(height * 1000 / width)
# # width = 1000
# # 调整当前图片的尺寸（同时也会压缩大小）
# dest = im.resize((1500, 2000), Image.ANTIALIAS)
# # 将图片保存并使用80%的质量进行压缩（继续压缩）
# dest.save('D:/new.jpg', quality=80)
#
# size = int(os.path.getsize('D:/new.jpg') / 1024)
# print("压缩图片大小为：%d KB" % size)



# source = '''
# <p style="text-align:left;text-indent:28px">
# <span style="font-size:14px;font-family:宋体">文章编辑完成后当然就得发布文章，某种意义上来说就是一个请求而已。但是要优化好整个发布功能，其实要考虑的问题是很多的。</span></p>
# <p><img src="/upload/image.png" title="image.png" alt="image.png"/></p>
# <p><span style="font-size:14px;font-family:宋体">首先要解决的问题是图片压缩的问题，作者发布文章时，并不会去关注图片有多大，只是简单的上传并确保前端能正常显示。</span></p>
# <p><img src="http://www.woniuxy.com/page/img/banner/newBank.jpg"/></p>
# <p><span style="font-size:14px;font-family:宋体">图片压缩分两种压缩方式，一种是压缩图片的尺寸，另外一种是压缩图片的大小。
# </span><img src="http://ww1.sinaimg.cn/large/68b02e3bgy1g2rzifbr5fj215n0kg1c3.jpg"/>
# </p>
# '''
#
# import re, requests
#
# # .* 贪婪模式（当前行查询最长匹配项）, 非贪婪模式：(匹配最短字符串） .+?
# list = re.findall('<img src="(.+?)"', source)
# print(list)
#
#
# for item in list:
#     if item.startswith('http://'):
#         resp = requests.get(item)
#         with open('D:/download.jpg', 'wb') as file:
#             file.write(resp.content)



# import socket                 # 引入Python的socket类
#
# s = socket.socket()
# s.connect(('127.0.0.1', 6379))   # 与Redis建立连接，并基于协议规则发送数据包
#
# s.send('*3\r\n'.encode())               # *3 表示发送的命令包含3个字符串
# s.send(b'$3\r\n')               # $3 表示接下来的字符串有3个字符
# s.send(b'set\r\n')
# s.send(b'$5\r\n')
# s.send(b'phone\r\n')
# s.send(b'$11\r\n')              # $11 表示接下来发的字符串有11个字符
# s.send(b'18812345678\r\n')
# r = s.recv(1024)               # 一条完整的命令发送完后接收Redis服务器响应
# print(r.decode())               # 输出 +OK 表示命令成功执行
#
# s.send(b'*2\r\n')
# s.send(b'$3\r\n')
# s.send(b'get\r\n')
# s.send(b'$5\r\n')
# s.send(b'phone\r\n')
# r = s.recv(1024)
# print(r.decode())               # 通过get命令读取变量phone的值



# import redis

# 指定Redis服务器的IP地址，端口号和数据库进行连接
# red = redis.Redis(host='127.0.0.1', port=6379, db=0)

# 使用连接池进行连接，推荐使用此方式
# pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True, db=0)
# red = redis.Redis(connection_pool=pool)
#
# print(red.get('phone'))
#
# red.hmset(name='mykey', mapping={'addr':'成都孵化园', 'tel':'028-12345678', 'employee':200})
# red.hset(name='mykey', key='name', value='蜗牛学院')    # 新增一条哈希值到mykey中
# red.hsetnx(name='mykey', key='name', value='蜗牛学院2') # 在mykey中不存在name时新增
# dict = red.hgetall('mykey')            # 获取mykey的所有值
# print(dict)



dict1 = '{"name":"蜗牛", "age":"3", "phone":"138383839438"}'
print(type(dict1))
dict = eval(dict1)
print(dict)
print(dict['name'])

import json
dict = json.loads(dict1)
print(dict['phone'])

