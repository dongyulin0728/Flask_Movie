from flask import Flask,render_template,request,redirect,url_for,session,g
from models import User
from exts import db
from pypinyin import lazy_pinyin
from decorators import login_required
import config
import  os
from sqlalchemy import or_
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/index/')
def index():
    return render_template('index.html')

@app.route('/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        print(telephone,password)
        user = User.query.filter(User.telephone == telephone ).first()
        if user and user.check_passwd(password):
            session['user_id'] = user.id
            #开启31天免密码登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return '手机号码错误'
@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('usename')
        password1 = request.form.get('passwd1')
        password2 = request.form.get('passwd2')
        #手机号码验证，如果注册就不能再次注册
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return '该手机号码已经注册，请换一个手机号码'
        else:
            #passwd1与passwd2是否相等
            if password1 != password2:
                return '两次输入的号码不想等'
            else:
                user = User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                #如果注册成功，就让页面跳转至登录页面
                return redirect(url_for('login'))
@app.route('/upload/',methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        file = request.files['reportFile']
        if file:
            filename = secure_filename(file.filename)
            if filename.startswith('.'):
                name = file.filename.split('.')[0]
                ext = file.filename.split('.')[1]
                filename = '_'.join(lazy_pinyin(name)) + '.' + ext
            else:
                name =file.filename.split('.')[0]
                ext = file.filename.split('.')[1]
                filename = '_'.join(lazy_pinyin(name)) + '.' + ext
            file.save(os.path.join("D:\\", filename))
            return '0'
    return render_template('upload.html')

if __name__ == '__main__':
    app.run()
