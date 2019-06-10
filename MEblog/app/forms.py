from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField,FileField
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo,Length,Required
from flask_wtf import FlaskForm
from flask_wtf.file import  FileRequired, FileAllowed
from app.models import User
from . import photos

class CommentForm(FlaskForm):
	body = TextAreaField('评论',validators=[Required(),Length(min=1)])
	submit = SubmitField('发表评论')

class hpForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, u'只能上传图片！'),
                                  FileRequired(u'请选择一个头像吧！')])
    submit = SubmitField(u'确认上传',render_kw={"class":"btn btn-primary"})

class ModifyBlog(FlaskForm):
    postitle = StringField('标题', validators=[DataRequired(message='请输入标题!')])
    postbody = TextAreaField('内容', validators=[DataRequired(message='请输入文章内容!')])
    submit = SubmitField('确定修改')

class ExitBlogTextForm(FlaskForm):
    postitle = StringField('标题', validators=[DataRequired(message='请输入标题!')])
    postbody = TextAreaField('内容', validators=[DataRequired(message='请输入文章内容!')])
    submit = SubmitField('发布文章')

class EditProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='请输入用户名!')])
    about_me = TextAreaField('关于我', validators=[Length(min=0, max=140)])
    submit = SubmitField('提交')

class LoginForm(FlaskForm):
    #DataRequired，当你在当前表格没有输入而直接到下一个表格时会提示你输入
    username = StringField('用户名',validators=[DataRequired(message='请输入名户名')])
    password = PasswordField('密码',validators=[DataRequired(message='请输入密码')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField(
        '重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')
    #校验用户名是否重复
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('用户名重复了，请您重新换一个呗!')
    #校验邮箱是否重复
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('邮箱重复了，请您重新换一个呗!')