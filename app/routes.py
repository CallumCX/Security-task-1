from flask import Blueprint, render_template, request, redirect, url_for

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
    return redirect(url_for('main.register'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    name = request.form.get('name') if request.method == 'POST' else ''
    return render_template('register.html', name=name)