import time

from flask import session
from sqlalchemy import Table, func
from common.database import dbconnect
from module.users import Users

dbsession, md, DBase = dbconnect()

class Article(DBase):
    __table__ = Table('article', md, autoload=True)

    # 查询所有文章
    def find_all(self):
        result = dbsession.query(Article).all()

    # 根据id查询文章，数据格式：(Article, 'nickname')
    def find_by_id(self, articleid):
        row = dbsession.query(Article, Users.nickname).join(Users,
            Users.userid == Article.userid).filter(
            Article.hidden == 0, Article.drafted == 0, Article.checked == 1,
            Article.articleid == articleid).first()
        return row

    # 指定分页的limit和offset的参数值，同时与用户表做连接查询
    def find_limit_with_users(self, start, count):
        result = dbsession.query(Article, Users.nickname).join(Users, Users.userid==Article.userid)\
            .filter(Article.hidden==0, Article.drafted==0, Article.checked==1)\
            .order_by(Article.articleid.asc()).limit(count).offset(start).all()
        return result

    # 统计一下当前文章的总数量
    def get_total_count(self):
        count = dbsession.query(Article).filter(Article.hidden==0, Article.drafted==0, Article.checked==1).count()
        return count

    # 根据文章类型获取文章
    def find_by_type(self, type, start, count):
        result = dbsession.query(Article, Users.nickname).join(Users,Users.userid == Article.userid) \
            .filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1, Article.type==type) \
            .order_by(Article.articleid.desc()).limit(count).offset(start).all()
        return result

    # 根据文章类型来获取总数量
    def get_count_by_type(self, type):
        count = dbsession.query(Article).filter(Article.hidden == 0,
                                                Article.drafted == 0,
                                                Article.checked == 1,
                                                Article.type == type).count()
        return count

    # 根据文章标题进行模糊搜索
    def find_by_headline(self, headline, start, count):
        result = dbsession.query(Article, Users.nickname).join(Users, Users.userid == Article.userid) \
            .filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1, Article.headline.like('%' + headline +'%')) \
            .order_by(Article.articleid.desc()).limit(count).offset(start).all()
        return result

    # 统计分页总数量
    def get_count_by_headline(self, headline):
        count = dbsession.query(Article).filter(Article.hidden == 0,
                                                Article.drafted == 0,
                                                Article.checked == 1,
                                                Article.headline.like('%' + headline +'%')).count()
        return count

    # 最新文章[(id, headline),(id, headline)]
    def find_last_9(self):
        result = dbsession.query(Article.articleid, Article.headline).\
            filter(Article.hidden==0, Article.drafted==0, Article.checked==1)\
            .order_by(Article.articleid.desc()).limit(9).all()
        return result

    # 最多阅读
    def find_most_9(self):
        result = dbsession.query(Article.articleid, Article.headline).\
            filter(Article.hidden==0, Article.drafted==0, Article.checked==1)\
            .order_by(Article.readcount.desc()).limit(9).all()
        return result

    # 特别推荐，如果超过9篇，可以考虑order by rand()的方式随机显示9篇
    def find_recommended_9(self):
        result = dbsession.query(Article.articleid, Article.headline).\
            filter(Article.hidden==0, Article.drafted==0, Article.checked==1, Article.recommended==1)\
            .order_by(func.rand()).limit(9).all()
        return result

    # 一次性返回三个推荐数据
    def find_last_most_recommended(self):
        last = self.find_last_9()
        most = self.find_most_9()
        recommended = self.find_recommended_9()
        return last, most, recommended

    # 每阅读一次文章，阅读次数+1
    def update_read_count(self, articleid):
        article = dbsession.query(Article).filter_by(articleid=articleid).first()
        article.readcount += 1
        dbsession.commit()

    # 根据文章编号查询文章标题
    def find_headline_by_id(self, articleid):
        row = dbsession.query(Article.headline).filter_by(articleid=articleid).first()
        return row.headline

    # 获取当前文章的上一篇和下一篇
    def find_prev_next_by_id(self, articleid):
        dict = {}

        # 查询比当前编号小的当中最大的一个
        row = dbsession.query(Article).filter(Article.hidden==0, Article.drafted==0, Article.checked==1,
              Article.articleid<articleid).order_by(Article.articleid.desc()).limit(1).first()
        # 如果当前已经是第一篇，上一篇也是当前文章
        if row is None:
            prev_id = articleid
        else:
            prev_id = row.articleid

        dict['prev_id'] = prev_id
        dict['prev_headline'] = self.find_headline_by_id(prev_id)


        # 查询比当前编号大的当中最小的一个
        row = dbsession.query(Article).filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1,
              Article.articleid > articleid).order_by(Article.articleid).limit(1).first()
        # 如果当前已经是最后一篇，下一篇也是当前文章
        if row is None:
            next_id = articleid
        else:
            next_id = row.articleid

        dict['next_id'] = next_id
        dict['next_headline'] = self.find_headline_by_id(next_id)

        return dict

    # 当发表或者回复评论后，为文章表字段replycount加1
    def update_replycount(self, articleid):
        row = dbsession.query(Article).filter_by(articleid=articleid).first()
        row.replycount += 1
        dbsession.commit()


    # 插入一篇新的文章，草稿或投稿通过参数进行区分
    def insert_article(self, type, headline, content, thumbnail, credit, drafted=0, checked=1):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        userid = session.get('userid')
        # 其他字段在数据库中均已设置好默认值，无须手工插入
        article = Article(userid=userid, type=type, headline=headline, content=content,
                          thumbnail=thumbnail, credit=credit, drafted=drafted,
                          checked=checked, createtime=now, updatetime=now)
        dbsession.add(article)
        dbsession.commit()

        return article.articleid  # 将新的文章编号返回，便于前端页面跳转

    # 根据文章编号更新文章的内容，可用于文章编辑或草稿修改，以及基于草稿的发布
    def update_article(self, articleid, type, headline, content, thumbnail, credit, drafted=0, checked=1):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        row = dbsession.query(Article).filter_by(articleid=articleid).first()
        row.type = type
        row.headline = headline
        row.content = content
        row.thumbnail = thumbnail
        row.credit = credit
        row.drafted = drafted

        row.checked = checked
        row.updatetime = now  # 修改文章的更新时间
        dbsession.commit()
        return articleid  # 继续将文章ID返回调用处


    # =========== 以下方法主要用于后台管理类操作 ================== #

    # 查询article表中除草稿外的所有数据并返回结果集
    def find_all_except_draft(self, start, count):
        result = dbsession.query(Article).filter(Article.drafted == 0).order_by(
            Article.articleid.desc()).limit(count).offset(start).all()
        return result

    # 查询除草稿外的所有文章的总数量
    def get_count_except_draft(self):
        count = dbsession.query(Article).filter(Article.drafted == 0).count()
        return count

    # 按照文章分类进行查询（不含草稿，该方法直接返回文章总数量用于分页）
    def find_by_type_except_draft(self, start, count, type):
        if type == 0:
            result = self.find_all_except_draft(start, count)
            total = self.get_count_except_draft()
        else:
            result = dbsession.query(Article).filter(Article.drafted == 0,
                     Article.type == type).order_by(Article.articleid.desc())\
                     .limit(count).offset(start).all()
            total = dbsession.query(Article).filter(Article.drafted == 0,
                     Article.type == type).count()
        return result, total    # 返回分页结果集和不分页的总数量

    # 按照标题模糊查询（不含草稿，不分页）
    def find_by_headline_except_draft(self, headline):
        result = dbsession.query(Article).filter(Article.drafted == 0,
                Article.headline.like('%' + headline + '%'))\
                .order_by(Article.articleid.desc()).all()
        return result

    # 切换文章的隐藏状态：1表示隐藏，0表示显示
    def switch_hidden(self, articleid):
        row = dbsession.query(Article).filter_by(articleid=articleid).first()
        if row.hidden == 1:
            row.hidden = 0
        else:
            row.hidden = 1
        dbsession.commit()
        return row.hidden   # 将当前最新状态返回给控制层

    # 切换文章的推荐状态：1表示推荐，0表示正常
    def switch_recommended(self, articleid):
        row = dbsession.query(Article).filter_by(articleid=articleid).first()
        if row.recommended == 1:
            row.recommended = 0
        else:
            row.recommended = 1
        dbsession.commit()
        return row.recommended

    # 切换文章的审核状态：1表示已审，0表示待审
    def switch_checked(self, articleid):
        row = dbsession.query(Article).filter_by(articleid=articleid).first()
        if row.checked == 1:
            row.checked = 0
        else:
            row.checked = 1
        dbsession.commit()
        return row.checked
