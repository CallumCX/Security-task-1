from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError, Regexp
import string, bleach, datetime


main = Blueprint('main', __name__, template_folder='templates')

@main.route('/', methods=['GET'])
def home():
    return redirect(url_for('main.register'))

def check_banned(form,field):
    if field.data in ["admin","root","superuser"]:
        current_app.logger.warning(f"Unable to register: Cannot use a blacklisted username! [IP:{request.remote_addr}, Username:{form.username.data}, Time:{datetime.datetime.now()}]")
        raise ValidationError("This username is not allowed! Blacklisted username!")

def valid_password(form,field):
    blacklisted_passwords = ["password123","admin","123456","qwerty","letmein","welcome","iloveyou","abc123","monkey","football"]
    if field.data in blacklisted_passwords:
        current_app.logger.warning(f"Unable to register: Cannot use a blacklisted password! [IP:{request.remote_addr}, Username:{form.username.data}, Time:{datetime.datetime.now()}]")
        raise ValidationError("This password is blacklisted! Blacklisted password!")

    if (form.username.data in field.data) or (form.email.data in field.data) and (form.username.data != form.email.data != ""):
        current_app.logger.warning(f"Unable to register: Username or Email cannot be in the password! [IP:{request.remote_addr}, Username:{form.username.data}, Time:{datetime.datetime.now()}]")
        raise ValidationError("This password must not contain the username or email!")

    number = False
    uppercase = False
    lowercase = False
    special = False

    for i in field.data:
        if i == " ":
            current_app.logger.warning(f"Unable to register: Cannot have whitespace in the password! [IP:{request.remote_addr}, Username:{form.username.data}, Time:{datetime.datetime.now()}]")
            raise ValidationError("This password can't contain whitespace!")
        else:
            if i.isalpha() and i.isupper():
                uppercase = True
            elif i.isalpha() and i.islower():
                lowercase = True
            elif i.isdigit():
                number = True
            elif i in string.punctuation:
                special = True

    if not (number and uppercase and lowercase and special):
        current_app.logger.warning(f"Unable to register: Password must contain an uppercase and lowercase character, a number and a special character! [IP:{request.remote_addr}, Username:{form.username.data}, Time:{datetime.datetime.now()}]")
        raise ValidationError("This password is invalid! Must contain 1 number, 1 uppercase, 1 lowercase and 1 special character!")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Field cannot be empty!"),Length(min=3,max=30,message="Invalid length!"),check_banned,Regexp(r"^[a-zA-z_]",message="Invalid characters!")])
    password = PasswordField('Password', validators=[DataRequired(message="Field cannot be empty!"),valid_password,Length(min=1,max=12,message="Invalid length!")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(message="Field cannot be empty!"),EqualTo('password',message="Passwords must match!")])
    email = EmailField('Email Address', validators=[DataRequired(message="Field cannot be empty!"),Email(message="Invalid format!"),Regexp(r".*\.(edu|ac\.uk|org)$",message="Invalid format!")])
    comment = StringField('Comment', validators=[DataRequired(message="Field cannot be empty!")])
    submit = SubmitField('Login')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        #email = form.email.data
        comment = bleach.clean(form.comment.data, tags=["b", "i", "u", "em", "strong", "a", "p", "ul", "ol", "li"],attributes={"a": ["href", "title"]}, strip=True)
        current_app.logger.info(f"Successfully registered: [IP::{request.remote_addr}, Username:{username}, Time:{datetime.datetime.now()}]")
        return "Successfully registered!", 200
    return render_template('register.html', form=form)