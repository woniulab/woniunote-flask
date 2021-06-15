from flask import session
from sqlalchemy import Table
from common.database import dbconnect
import time

dbsession, md, DBase = dbconnect()

class Credit(DBase):
    __table__ = Table('credit', md, autoload=True)

    # 插入积分明细数据
    def insert_detail(self, type, target, credit):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        credit = Credit(userid=session.get('userid'), category=type, target=target,
                        credit=credit, createtime=now, updatetime=now)
        dbsession.add(credit)
        dbsession.commit()

    # 判断用户是否已经消耗积分
    def check_payed_article(self, articleid):
        result = dbsession.query(Credit).filter_by(userid=session.get('userid'), target=articleid).all()
        if len(result) > 0:
            return True
        else:
            return False
