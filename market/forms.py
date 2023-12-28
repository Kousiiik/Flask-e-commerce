from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, ValidationError, EqualTo, Email, DataRequired
from market.models import User


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('This username is Already exist , please try different username')

    def validate_email_address(self, email_address_to_check):
        email = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email:
            raise ValidationError('Email_address is Already exist , please try different email')

    username = StringField(label='username', validators=[Length(min=2, max=30), DataRequired()])

    email_address = StringField(label='Email', validators=[Email(), DataRequired(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6)])
    password2 = PasswordField(label='confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='submit')


# pip install flask_login
class LoginForm(FlaskForm):
    username = StringField(label='username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='submit')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item')
