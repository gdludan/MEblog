from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import db,login
from hashlib import md5

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    email = db.Column(db.String(120),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.now)
    head_portrait=db.Column(db.String(255),default=r'../static/images/default.jpg')
    reg_time=db.Column(db.DateTime, default=datetime.now)
    # back是反向引用,User和Post是一对多的关系，backref是表示在Post中新建一个属性author，关联的是Post中的user_id外键关联的User对象。
    #lazy属性常用的值的含义，select就是访问到属性的时候，就会全部加载该属性的数据;joined则是在对关联的两个表进行join操作，从而获取到所有相关的对象;dynamic则不一样，在访问属性的时候，并没有在内存中加载数据，而是返回一个query对象, 需要执行相应方法才可以获取对象，比如.all()
    posts = db.relationship('Post',backref='author',lazy='dynamic')

    def __repr__(self):
        return '<用户名:{}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key=True)
    postitle = db.Column(db.Text)
    postbody = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.now)
    user_id = db .Column(db.Integer,db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post   {}   {}>'.format(self.postitle,self.postbody)
    def set_postitle(self, postitle):
        self.postitle = postitle
    def set_postbody(self, postbody):
        self.postbody = postbody
    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

class UPFile(db.Model):
    __tablename__ = 'upfiles'
    id = db.Column(db.Integer, primary_key=True)
    filename=db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<UPFile:{}>'.format(self.filename)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db .Column(db.Integer,db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Comment: {}>'.format(self.body)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))