from flask import session
from sqlalchemy import Table
from common.database import dbconnect
import time, random

from module.article import Article

dbsession, md, DBase = dbconnect()

class Favorite(DBase):
    __table__ = Table('favorite', md, autoload=True)

    # 播入文章收藏数据
    def insert_favorite(self, articleid):
        row = dbsession.query(Favorite).filter_by(articleid=articleid, userid=session.get('userid')).first()
        if row is not None:
            row.canceled = 0
        else:
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            favorite = Favorite(articleid=articleid, userid=session.get('userid'),canceled=0,createtime=now, updatetime=now)
            dbsession.add(favorite)
        dbsession.commit()

    # 取消收藏
    def cancel_favorite(self, articleid):
        row = dbsession.query(Favorite).filter_by(articleid=articleid, userid=session.get('userid')).first()
        row.canceled = 1
        dbsession.commit()

    # 判断是否已经被收藏
    def check_favorite(self, articleid):
        row = dbsession.query(Favorite).filter_by(articleid=articleid, userid=session.get('userid')).first()
        if row is None:
            return False
        elif row.canceled == 1:
            return False
        else:
            return True

    # 为用户中心查询我的收藏添加数据操作方法
    def find_my_favorite(self):
        result = dbsession.query(Favorite, Article).join(Article, Favorite.articleid ==
                Article.articleid).filter(Favorite.userid == session.get('userid')).all()
        return result

    # 切换收藏和取消收藏的状态
    def switch_favorite(self, favoriteid):
        row = dbsession.query(Favorite).filter_by(favoriteid=favoriteid).first()
        if row.canceled == 1:
            row.canceled = 0
        else:
            row.canceled = 1
        dbsession.commit()
        return row.canceled