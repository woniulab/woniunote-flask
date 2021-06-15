from datetime import datetime
import re
import redis
from common.database import dbconnect
from common.utility import model_list
from module.article import Article
from module.users import Users

def redis_connect():
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True, db=0)
    red = redis.Redis(connection_pool=pool)
    return red

# def redis_mysql_string():
#     from common.database import dbconnect
#
#     red = redis_connect()  # 连接到Redis服务器
#
#     # 获取数据库连接信息
#     dbsession, md, DBase = dbconnect()
#
#     # 查询users表的所有数据，并将其转换为JSON
#     result = dbsession.query(Users).all()
#     json = model_list(result)
#
#     red.set('users', str(json))  # 将整张表的数据保存成JSON字符串


def redis_mysql_string():
    from common.database import dbconnect

    red = redis_connect()  # 连接到Redis服务器

    # 获取数据库连接信息
    dbsession, md, DBase = dbconnect()

    # 查询users表的所有数据，并将其转换为JSON
    result = dbsession.query(Users).all()
    user_list = model_list(result)
    for user in user_list:
        red.set(user['username'], user['password'])


def redis_mysql_hash():
    from common.database import dbconnect

    red = redis_connect()  # 连接到Redis服务器

    # 获取数据库连接信息
    dbsession, md, DBase = dbconnect()

    # 查询users表的所有数据，并将其转换为JSON
    result = dbsession.query(Users).all()
    user_list = model_list(result)
    for user in user_list:
        red.hset('users_hash', user['username'], str(user))


def redis_article_zsort():

    dbsession, md, DBase = dbconnect()
    result = dbsession.query(Article, Users.nickname).join(Users, Users.userid == Article.userid).all()
    # result的数据格式为：[ (<__main__.Article object at 0x113F9150>, '强哥')，() ]
    # 对result进行遍历处理，最终生成一个标准的JSON数据结构

    list = []
    for article, nickname in result:
        dict = {}
        for k, v in article.__dict__.items():
            if not k.startswith('_sa_instance_state'):  # 跳过内置字段
                # 如果某个字段的值是datetime类型，则将其格式为字符串
                if isinstance(v, datetime):
                    v = v.strftime('%Y-%m-%d %H:%M:%S')
                # 将文章内容的HTML和不可见字符删除，再截取前面80个字符
                elif k == 'content':
                    pattern = re.compile(r'<[^>]+>')
                    temp = pattern.sub('', v)
                    temp = temp.replace('&nbsp;', '')
                    temp = temp.replace('\r', '')
                    temp = temp.replace('\n', '')
                    temp = temp.replace('\t', '')
                    v = temp.strip()[0:80]
                dict[k] = v
        dict['nickname'] = nickname
        list.append(dict)  # 最终构建一个标准的列表+字典的数据结构

    # 将数据缓存到有序集合中
    red = redis_connect()
    for row in list:
        # zadd的命令参数为：（键名，{值:排序依据})
        # 此处将文章表中的每一行数据作为值，文章编号作为排序依据
        red.zadd('article', {str(row): row['articleid']})


if __name__ == '__main__':
    # redis_mysql_hash()
    redis_article_zsort()