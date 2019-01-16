from wtforms import Form, StringField, IntegerField, PasswordField
from wtforms.validators import Length, NumberRange, DataRequired, Email, ValidationError
from app.models.user import User


class RegisterForm(Form):
    nickname = StringField(validators=[DataRequired(), Length(2, 10, message='昵称至少两个字符，最多10个字符')])
    email = StringField(validators=[DataRequired(), Length(min=8, max=64), Email(message='电子邮件格式错误')])
    password = PasswordField(validators=[Length(min=6, max=32), DataRequired(message='密码不能为空')])

    # 自定义验证器
    def validate_email(self, field):
        """
        validate_email函数名中的email，会帮助定位到email，表名这个验证器是email的验证器
        :param field:  field代表传入的email参数
        :return:
        """
        if User.query.filter_by(email=field.data).first():  # filter_by可以传入一组查询条件
            raise ValidationError('电子邮件已被注册')  # validators特有的异常

    def validate_nickname(self, field):

        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('该昵称已被注册')


class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(min=8, max=64), Email(message='电子邮件格式错误')])
    password = PasswordField(validators=[Length(min=6, max=32), DataRequired(message='密码不能为空')])