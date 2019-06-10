from flask import Flask
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from config import Config
#创建app应用,__name__是python预定义变量，被设置为使用本模块.
app = Flask(__name__)
#添加配置信息
app.config.from_object(Config)
#建立数据库关系
db = SQLAlchemy(app)
#绑定app和数据库，以便进行操作
migrate = Migrate(app,db)
#登陆模块
login = LoginManager(app)
# 在login = LoginManager(app)后面加上即可
login.login_view = 'login'

photos = UploadSet('photos',IMAGES)
configure_uploads(app,photos)
patch_request_class(app)

moment = Moment(app)
bootstrap = Bootstrap(app)
#如果你使用的IDE，在routes这里会报错，因为我们还没有创建呀，为了一会不要再回来写一遍，因此我先写上了
from app import routes,models