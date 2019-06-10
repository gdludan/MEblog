import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    FLASKY_COMMENTS_PER_PAGE=10
    POSTS_PER_PAGE = 10
    # 设置密匙要没有规律，别被人轻易猜到哦
    # SECRET_KEY = 'a9087FFJFF9nnvc2@#$%FSD'
    SECRET_KEY = '65396ee4aad0b4f17aacd1c6112ee364'
    UPLOADED_PHOTOS_DEST = os.path.abspath(os.path.join(os.getcwd(), "app/static/uploads/hp"))
	username = "root"
	password = "root"
	db_name = "blog"
	db_code = "utf8"
    #格式为mysql+pymysql://数据库用户名:密码@数据库地址:端口号/数据库的名字?数据库格式
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@localhost:3306/%s?charset=%s'%(username,password,db_name,db_code)
    #如果你不打算使用mysql，使用这个连接sqlite也可以
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR,'app.db')
	#如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
    SQLALCHEMY_TRACK_MODIFICATIONS = False