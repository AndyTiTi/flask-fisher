from wtforms import Form, StringField, IntegerField, PasswordField
from wtforms.validators import Length, NumberRange, DataRequired, Email, ValidationError, EqualTo
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


class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(min=8, max=64), Email(message='电子邮件格式错误')])

class ChangePasswordForm(Form):
    old_password = PasswordField('原有密码', validators=[DataRequired()])
    new_password1 = PasswordField('新密码', validators=[
        DataRequired(), Length(6, 10, message='密码长度至少需要在6到20个字符之间'),
        EqualTo('new_password2', message='两次输入的密码不一致')])
    new_password2 = PasswordField('确认新密码字段', validators=[DataRequired()])

class ResetPasswordForm(Form):
    passowrd1 = PasswordField(validators=[DataRequired(), Length(6, 32, message='密码长度在6-32个字符之间'), ])
    password2 = PasswordField(validators=[DataRequired(), Length(6, 32), EqualTo('password1', message='两次输入的密码不同')])
