from flask import Blueprint, request, session, jsonify

from module.article import Article
from module.comment import Comment
from module.credit import Credit
from module.users import Users

comment = Blueprint('comment', __name__)

@comment.before_request
def before_comment():
    if session.get('islogin') is None or session.get('islogin') != 'true':
        # return '你还没有登录，不能发表评论'
        return 'not-login'

@comment.route('/comment', methods=['POST'])
def add():
    articleid = request.form.get('articleid')
    content = request.form.get('content').strip()
    ipaddr = request.remote_addr

    # 对评论内容进行简单检验
    if len(content) < 5 or len(content) > 1000:
        return 'content-invalid'

    comment = Comment()
    if not comment.check_limit_per_5():
        try:
            comment.insert_comment(articleid, content, ipaddr)
            # 评论成功后，更新积分明细和剩余积分，及文章回复数量
            Credit().insert_detail(type='添加评论', target=articleid, credit=2)
            Users().update_credit(2)
            Article().update_replycount(articleid)
            return 'add-pass'
        except:
            return 'add-fail'
    else:
        return 'add-limit'


@comment.route('/reply', methods=['POST'])
def reply():
    articleid = request.form.get('articleid')
    commentid = request.form.get('commentid')
    content = request.form.get('content').strip()
    ipaddr = request.remote_addr

    # 如果评论的字数低于5个或多于1000个，均视为不合法
    if len(content) < 5 or len(content) > 1000:
        return 'content-invalid'

    comment = Comment()
    # 没有超出限制才能发表评论
    if not comment.check_limit_per_5():
        try:
            comment.insert_reply(articleid=articleid, commentid=commentid,
                                 content=content, ipaddr=ipaddr)
            # 评论成功后，同步更新credit表明细、users表积分和article表回复数
            Credit().insert_detail(type='回复评论', target=articleid, credit=2)
            Users().update_credit(2)
            Article().update_replycount(articleid)
            return 'reply-pass'
        except:
            return 'reply-fail'
    else:
        return 'reply-limit'


# 为了使用Ajax分页，特创建此接口作为演示
# 由于分页栏已经完成渲染，此接口仅根据前端的页码请求后台对应数据
@comment.route('/comment/<int:articleid>-<int:page>')
def comment_page(articleid, page):
    start = (page - 1) * 10
    comment = Comment()
    list = comment.get_comment_user_list(articleid, start, 10)
    return jsonify(list)
