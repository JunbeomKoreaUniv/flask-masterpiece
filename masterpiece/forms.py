from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class SongForm(FlaskForm):
    name = StringField('곡명', validators=[DataRequired('곡명은 필수입력 항목입니다')])
    singer = StringField('가수', validators=[DataRequired('가수는 필수입력 항목입니다')])

class ReviewForm(FlaskForm):
    content = TextAreaField('후기', validators=[DataRequired('후기는 필수입력 항목입니다.')])
    rate = FloatField('평점', validators=[DataRequired('평점은 필수입력 항목입니다.')])

class UserCreateForm(FlaskForm):
    user_email_id = EmailField('이메일', validators=[DataRequired('email id를 입력해주세요'), Email()])
    user_name = StringField('사용자명', validators=[DataRequired('사용자명을 입력해주세요')])
    password1 = PasswordField('비밀번호', validators=[DataRequired('비밀번호를 입력해주세요'), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired('비밀번호확인을 입력해주세요')])
    
class UserLoginForm(FlaskForm):
    user_email_id = EmailField('이메일', validators=[DataRequired('email id를 입력해주세요'), Email()])
    password = PasswordField('비밀번호', validators=[DataRequired('비밀번호를 입력해주세요')])