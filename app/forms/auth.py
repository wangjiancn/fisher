# coding = utf-8
from wtforms import Form, StringField, IntegerField, PasswordField
from wtforms.validators import Length, NumberRange, DataRequired, Email, ValidationError
from app.models.base import db
from app.models.user import User


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message="电子邮箱不符合规范")])
    password = PasswordField(validators=[DataRequired(message='密码不可以为空，请输入你的密码'),Length(6,32)])
    nickname = StringField(validators=[DataRequired(),Length(2,10,message='昵称至少需要两个字符，最多不超过10个字符')])

    # todo 自定义验证器，函数以validate_ + 校验对象名 作为名字
    def validate_email(self, field):
        # db.session.
        if User.query.filter_by(email = field.date).first():
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self, field):
        # db.session.
        if User.query.filter_by(email = field.date).first():
            raise ValidationError('昵称已被注册')

class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message="电子邮箱不符合规范")])
    password = PasswordField(validators=[DataRequired(message='密码不可以为空，请输入你的密码'),Length(6,32)])
