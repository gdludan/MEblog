#从app模块中即从__init__.py中导入创建的app应用
from app.forms import LoginForm,RegistrationForm,EditProfileForm,ExitBlogTextForm,ModifyBlog,hpForm,CommentForm
from flask_login import current_user,login_user,logout_user,login_required
from flask import render_template,flash,redirect,url_for,jsonify
from werkzeug.utils import secure_filename # 使用这个是为了确保filename是安全的
from app.models import User,Post,UPFile,Comment
from werkzeug.urls import url_parse
from flask_restful import request
from datetime import datetime
from app import app,db
from os import path
import random,time,os
from . import photos

def url():return request.url.rstrip(request.path)
def file_extension(path):return path.splitext(path)[1]
def rand_number():return str(int(round(time.time()*1000)))+str(random.randint(0,4096))
def upload_file(filename):
    u = User.query.filter_by(username=current_user.username).first()
    db.session.add(UPFile(filename=filename, user_id=u.id))
    db.session.commit()
    return True
'''
url:取当前网址
file_extension:取文件拓展名
rand_number:取随机数字
upload_file:写入上传文件名
'''
#建立路由，通过路由可以执行其覆盖的方法，可以多个路由指向同一个方法。
@app.route('/')
@app.route('/index')
#这样，必须登录后才能访问首页了,会自动跳转至登录页
#@login_required
def index():
    page=request.args.get('page',1,type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=10, error_out=False)
    posts,post = pagination.items,[]
    for i in posts:
        user=User.query.filter_by(id=i.user_id).first_or_404()
        temp = {'author': user, 'postbody': i.postbody, 'alink': '../id/' + str(i.id), 'user_id': i.user_id,
                'postitle': i.postitle, 'timestamp': i.timestamp, 'bloglink': '../modify_tinymce_blog/' + str(i.id),
                'id': i.id}
        post.append(temp)
    return render_template('blog/index.html', posts=post, pagination=pagination,title='欢迎来到我的博客')
@app.route('/test')
def test():
    return render_template('Expand/test.html')

###################下面是测试好的代码########################
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('你的提交已变更.')
        return redirect(url_for('user', username=current_user.username))
    else:
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('blog/edit_profile.html', title='个人资料编辑',form=form)
@app.route('/user/<username>')
@login_required
def user(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    pagination = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).\
        paginate(page=page, per_page=10,error_out=False)
    posts,post = pagination.items,[]
    for i in posts:
        user=User.query.filter_by(id=i.user_id).first_or_404()
        temp = {'author': user, 'postbody': i.postbody, 'postlink': '../id/' + str(i.id), 'user_id': i.user_id,
                'postitle': i.postitle, 'timestamp': i.timestamp, 'bloglink': '../modify_tinymce_blog/' + str(i.id),
                'id': i.id}
        post.append(temp)
    return render_template('blog/user.html', user=user, posts=post, pagination=pagination,title=user.username)
@app.route('/id/<postid>',methods=['GET','POST'])
def post_id(postid):
    page = request.args.get('page', 1, type=int)
    posts,comments,url={},[],request.url
    p,form= Post.query.filter_by(id=postid).first_or_404(),CommentForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=current_user.username).first_or_404()
        comment = Comment(body=form.body.data,post_id=p.id,user_id=user.id)
        print(Comment)
        db.session.add(comment)
        db.session.commit()
        flash('你的评论已经发表了。')
        if '?' in url: url = url.split('?')[0]
        return redirect(url)
    elif request.method =='GET':
        if '?' in url :url=url.split('?')[0]
        pagination = Comment.query.filter_by(post_id=p.id).order_by(Comment.timestamp.desc()).\
                paginate(page=page, per_page=10,error_out=False)
        for info in pagination.items:
            u=User.query.filter_by(id=info.user_id).first_or_404()
            comment={'id':info.id,'body':info.body,'post_id':info.post_id,
                     'user_id':info.user_id,'timestamp':info.timestamp,'user':u}
            comments.append(comment)
        posts = {'postbody':p.postbody,'postitle':p.postitle,'user_id':p.user_id,
                 'timestamp':p.timestamp,'id':p.id}
    return render_template('blog/blog_text.html', posts=posts,title=p.postitle,
                           pagination=pagination,comments=comments,url=url,form=form)
@app.route('/editor', methods=['GET', 'POST'])
@login_required
def editor():
    #如果是post方法就返回tinymce生成html代码，否则渲染editor.html
    u = User.query.filter_by(username=current_user.username).first()
    if request.method=='POST':
        db.session.add(Post(postitle=request.form['title'], postbody=request.form['content'], author=u))
        db.session.commit()
        flash('文章已发布.')
        return redirect(url_for('user', username=current_user.username))
    return render_template('Expand/editor.html',title=current_user.username+'--添加文章',cnt={})
@app.route('/modify_tinymce_blog/<id>', methods=['GET', 'POST'])
@login_required
def modify_tinymce_blog(id):
    p,cnt = Post.query.filter_by(id=id).first_or_404(),{}
    if request.method == 'POST':
        post = Post.query.filter_by(id=id).first()
        post.postitle,post.postbody=request.form['title'],request.form['content']
        db.session.commit()
        flash('文章已修改.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        cnt={'title':p.postitle,'cnt':p.postbody}
    return render_template('Expand/editor.html', title='编辑文章',cnt=cnt)
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    #判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    #对表格数据进行验证
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('无效的用户名或密码')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # 此时的next_page记录的是跳转至登录页面是的地址
        next_page = request.args.get('next')
        # 如果next_page记录的地址不存在那么就返回首页
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        # 综上，登录后要么重定向至跳转前的页面，要么跳转至首页
        return redirect(next_page)
    return render_template('blog/login.html',title='登录',form=form)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
@app.route('/register', methods=['GET', 'POST'])
def register():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜你成为我们网站的新用户!')
        return redirect(url_for('login'))
    return render_template('blog/register.html', title='注册', form=form)
@app.route("/upload",methods=['GET','POST'])
@login_required
def upload():
    page = request.args.get('page', 1, type=int)
    up_path=os.getcwd()+'\\app'
    upfiles = []
    if request.method=='POST':
        f = request.files["file"]
        size=len(request.files["file"].read())
        if size > 20*1024*1024:
            flash('上传文件失败，文件超出20Mb')
            flash('你上传的文件大小为'+str(round(size/1024/1024,2))+'Mb')
            return redirect(url_for('upload'))
        else:
            base_path =  path.abspath(path.dirname(__file__))
            upload_path = path.join(base_path,'static/uploads/')
            file_name = upload_path + secure_filename(f.filename)
            f.seek(0,0)
            f.save(file_name)
            if upload_file(filename='../'+file_name.lstrip(up_path)):
                flash('成功上传【'+f.filename+'】')
                return redirect(url_for('upload'))
            else:
                flash('上传文件失败，数据库写入失败')
                return redirect(url_for('upload'))
    else:
        u = User.query.filter_by(username=current_user.username).first()
        pagination = UPFile.query.filter_by(user_id=u.id).order_by(UPFile.timestamp.desc()).\
            paginate(page=page, per_page=10,error_out=False)
        print(pagination.items)
        for upfile in pagination.items:
            title = upfile.filename.split('/')[3]
            temp = {'url': upfile.filename, 'title': title,'time':upfile.timestamp}
            upfiles.append(temp)
    return render_template('Expand/upload.html',title='上传文件',upfiles=upfiles,pagination=pagination)
@app.route('/head_portrait',methods=['GET','POST'])
@login_required
def head_portrait():
    form = hpForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
        current_user.head_portrait = '../'+file_url.lstrip(url())
        db.session.add(current_user)
        db.session.commit()
        flash('修改成功!')
        return redirect(url_for('.user', username=current_user.username, file_url=file_url))
    return render_template('Expand/edit_gravatar.html', form=form, file_url=current_user.head_portrait,title='更换头像')
@app.route('/post/<int:post_id>/delete',methods=['post'])
@login_required
def post_delete(post_id):
    res = {
        "status": 1,
        "message": "成功"
    }
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        res['status'] = 404
        res["message"] = "找不到文件"
        flash('删除失败')
        return jsonify(res)
    else:
        Post.query.filter_by(id=post_id).delete()
        db.session.commit()
        flash('删除成功')
        return jsonify(res)
###################下面是请求错误时跳转页面########################
@app.errorhandler(400)
def page_not_found(e):
    error={'number':400,'title':'请求无效','data':'Bad request 无效的请求'}
    return render_template('blog/error.html',error=error), 400
@app.errorhandler(403)
def page_not_found(e):
    error={'number':403,'title':'禁止访问','data':'服务器禁止访问'}
    return render_template('blog/error.html',error=error), 403
@app.errorhandler(404)
def page_not_found(e):
    error={'number':404,'title':'找不到页面','data':'找不到文件'}
    return render_template('blog/error.html',error=error), 404
@app.errorhandler(410)
def page_not_found(e):
    error={'number':410,'title':'gone ','data':'gone '}
    return render_template('blog/error.html',error=error), 410
@app.errorhandler(500)
def internal_server_error(e):
    error={'number':500,'title':'服务器错误','data':'服务器内部错误'}
    return render_template('blog/error.html',error=error), 500
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()