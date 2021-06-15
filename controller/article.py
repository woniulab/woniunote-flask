import os

from flask import Blueprint, abort, render_template, request, session

from common.utility import parse_image_url, generate_thumb
from module.article import Article
from module.comment import Comment
from module.credit import Credit
from module.favorite import Favorite
from module.users import Users
import math

article = Blueprint("article", __name__)

@article.route('/article/<int:articleid>')
def read(articleid):
    try:
        # 数据格式：(Article, 'nickname')
        result = Article().find_by_id(articleid)
        if result is None:
            abort(404)
    except:
        abort(500)

    dict = {}
    for k, v in result[0].__dict__.items():
        if not k.startswith('_sa_instance_state'):
            dict[k] = v
    dict['nickname'] = result.nickname

    # 如果已经消耗积分，则不再截取文章内容
    payed = Credit().check_payed_article(articleid)

    position = 0
    if not payed:
        content = dict['content']
        temp = content[0:int(len(content)/2)]
        position = temp.rindex('</p>') + 4
        dict['content'] = temp[0:position]

    Article().update_read_count(articleid)  # 阅读次数+1

    is_favorited = Favorite().check_favorite(articleid)

    # 获取当前文章的上一篇和下一篇
    prev_next = Article().find_prev_next_by_id(articleid)

    # 显示当前文章对应的评论
    # comment_user = Comment().find_limit_with_user(articleid, 0, 50)

    # comment_list = Comment().get_comment_user_list(articleid, 0, 10)
    #
    count = Comment().get_count_by_article(articleid)
    total = math.ceil(count / 10)

    return render_template('article-user.html', article=dict, position=position, payed=payed,
                           is_favorited=is_favorited, prev_next=prev_next,
                           total=total)


@article.route('/readall', methods=['POST'])
def read_all():
    position = int(request.form.get('position'))
    articleid = request.form.get('articleid')
    article = Article()
    result = article.find_by_id(articleid)
    content = result[0].content[position:]

    # 如果已经消耗积分，则不再扣除
    payed = Credit().check_payed_article(articleid)
    if not payed:
        # 添加积分明细
        Credit().insert_detail(type='阅读文章', target=articleid, credit=-1*result[0].credit)
        # 减少用户表的剩余积分
        Users().update_credit(credit=-1*result[0].credit)

    return content

@article.route('/prepost')
def pre_post():
    return render_template('post-user.html')

@article.route('/article', methods=['POST'])
def add_article():
    headline = request.form.get('headline')
    content = request.form.get('content')
    type = int(request.form.get('type'))
    credit = int(request.form.get('credit'))
    drafted = int(request.form.get('drafted'))
    checked = int(request.form.get('checked'))
    articleid = int(request.form.get('articleid'))

    if session.get('userid') is None:
        return 'perm-denied'
    else:
        user = Users().find_by_userid(session.get('userid'))
        if user.role == 'editor':
            # 权限合格，可以执行发布文章的代码
            # 首先为文章生成缩略图，优先从内容中找，找不到则随机生成一张
            url_list = parse_image_url(content)
            if len(url_list) > 0:   # 表示文章中存在图片
                thumbname = generate_thumb(url_list)
            else:
                # 如果文章中没有图片，则根据文章类别指定一张缩略图
                thumbname = '%d.png' % type

            article = Article()
            # 再判断articleid是否为0，如果为0则表示是新数据
            if articleid == 0:
                try:
                    id = article.insert_article(type=type, headline=headline, content=content, credit=credit,
                                                thumbnail=thumbname,drafted=drafted, checked=checked)

                    # 新增文章成功后，将已经静态化的文章列表页面全部删除，便于生成新的静态文件
                    list = os.listdir('./template/index-static/')
                    for file in list:
                        os.remove('./template/index-static/' + file)

                    return str(id)
                except Exception as e:
                    return 'post-fail'
            else:
                # 如果是已经添加过的文章，则做修改操作
                try:
                    id = article.update_article(articleid=articleid, type=type,
                                                headline=headline, content=content, credit=credit,
                                                thumbnail=thumbname, drafted=drafted, checked=checked)
                    return str(id)
                except:
                    return 'post-fail'

        # 如果角色不是作者，则只能投稿，不能正式发布
        elif checked == 1:
                return 'perm-denied'
        else:
            return 'perm-denied'
