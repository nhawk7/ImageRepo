from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from imagerepo.models import User


# create forms

class Register(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=16)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=16)])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # make sure username is unique
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exists")


class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=16)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=16)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class Upload(FlaskForm):
    image = FileField('Upload image:', validators=[DataRequired(), FileAllowed(['png'])])
    submit = SubmitField('Upload')


class SearchUser(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=16)])
    submit = SubmitField('Search')

    # make sure username exists
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError("User not found")
