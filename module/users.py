from flask import session
from sqlalchemy import Table
from common.database import dbconnect
import time, random

dbsession, md, DBase = dbconnect()

class Users(DBase):
    __table__ = Table('users', md, autoload=True)

    # 查询用户名，可用于注册时判断用户名是否已注册，也可用于登录校验
    def find_by_username(self, username):
        result = dbsession.query(Users).filter_by(username=username).all()
        return result

    # 实现注册，首次注册时用户只需要输入用户名和密码，所以只需要两个参数
    # 注册时，在模型类中为其他字段尽力生成一些可用的值，虽不全面，但可用
    # 通常用户注册时不建议填写太多资料，影响体验，可待用户后续逐步完善
    def do_register(self, username, password):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        nickname = username.split('@')[0]  # 默认将邮箱账号前缀作为昵称
        avatar = str(random.randint(1, 15))  # 从15张头像图片中随机选择一张
        user = Users(username=username, password=password, role='user', credit=50,
                     nickname=nickname, avatar=avatar + '.png', createtime=now, updatetime=now)
        dbsession.add(user)
        dbsession.commit()
        return user

    # 修改用户剩余积分，积分为正数表示增加积分，为负数表示减少积分
    def update_credit(self, credit):
        user = dbsession.query(Users).filter_by(userid=session.get('userid')).one()
        user.credit = int(user.credit) + credit
        dbsession.commit()

    def find_by_userid(self, userid):
        user = dbsession.query(Users).filter_by(userid=userid).one()
        return user