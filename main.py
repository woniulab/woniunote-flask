from flask import Flask, abort, render_template
import os
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()    # ModuleNotFoundError: No module named 'MySQLdb'

app = Flask(__name__, template_folder='template', static_url_path='/', static_folder='resource')
app.config['SECRET_KEY'] = os.urandom(24)

# 使用集成方式处理SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/woniunote?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # True: 跟踪数据库的修改，及时发送信号
app.config['SQLALCHEMY_POOL_SIZE'] = 100  # 数据库连接池的大小。默认是数据库引擎的默认值（通常是 5）
# 实例化db对象
db = SQLAlchemy(app)

# 定义404错误页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error-404.html')

# 定义500错误页面
@app.errorhandler(500)
def server_error(e):
    return render_template('error-500.html')

# 定义全局拦截器，实现自动登录
@app.before_request
def before():
    url = request.path

    pass_list = ['/user', '/login', '/logout']
    if url in pass_list or url.endswith('.js') or url.endswith('.jpg'):
        pass

    elif session.get('islogin') is None:
        username = request.cookies.get('username')
        password = request.cookies.get('password')
        if username != None and password != None:
            user = Users()
            result = user.find_by_username(username)
            if len(result) == 1 and result[0].password == password:
                session['islogin'] = 'true'
                session['userid'] = result[0].userid
                session['username'] = username
                session['nickname'] = result[0].nickname
                session['role'] = result[0].role

# 通过自定义过滤器来重构truncate原生过滤器
def mytruncate(s, length, end='...'):
    count = 0
    new = ''
    for c in s:
        new += c  # 每循环一次，将一个字符添加到new字符串后面
        if ord(c) <= 128:
            count += 0.5
        else:
            count += 1
        if count > length:
            break
    return new + end
# 注册mytruncate过滤器
app.jinja_env.filters.update(truncate=mytruncate)

# 定义文章类型函数，供模板页面直接调用
@app.context_processor
def gettype():
    type = {
        '1': 'PHP开发',
        '2': 'Java开发',
        '3': 'Python开发',
        '4': 'Web前端',
        '5': '测试开发',
        '6': '数据科学',
        '7': '网络安全',
        '8': '蜗牛杂谈'
    }
    return dict(article_type=type)

@app.route('/preupload')
def pre_upload():
    return render_template('file-upload.html')

@app.route('/upload', methods=['POST'])
def do_upload():
    headline = request.form.get('headline')
    content = request.form.get('content')
    file = request.files.get('upfile')
    print(headline, content)  # 可以正常获取表单元素的值

    suffix = file.filename.split('.')[-1]  # 取得文件的后缀名
    # 也可以根据文件的后缀名对文件类型进行过滤，如：
    if suffix.lower() not in ['jpg', 'jpeg', 'png', 'rar', 'zip', 'doc', 'docx']:
        return 'Invalid'

    # 将文件保存到某个目录中
    file.save('D:/test001.' + suffix)
    return 'Done'

if __name__ == '__main__':
    from controller.index import *
    app.register_blueprint(index)

    from controller.user import *
    app.register_blueprint(user)

    from controller.article import *
    app.register_blueprint(article)

    from controller.favorite import *
    app.register_blueprint(favorite)

    from controller.comment import *
    app.register_blueprint(comment)

    from controller.ueditor import *
    app.register_blueprint(ueditor)

    from controller.admin import *
    app.register_blueprint(admin)

    from controller.ucenter import *
    app.register_blueprint(ucenter)

    app.run(debug=True)