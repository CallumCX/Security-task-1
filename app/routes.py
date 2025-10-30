from flask import Blueprint, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo, Length, Email

main = Blueprint('main', __name__, template_folder='templates')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=3,max=30)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    email = EmailField('Email Address', validators=[DataRequired(),Email()])
    submit = SubmitField('Login')

@main.route('/', methods=['GET'])
def home():
    return redirect(url_for('main.register'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        return "successfully registered your account"
    return render_template('register.html', form=form)