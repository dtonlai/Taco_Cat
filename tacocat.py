from flask import Flask, render_template, redirect, url_for, g
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required

import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = "asdjfoadsgugkgnigi090j3onfo3inojfojklsnl"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view('login')

@app.before_request
def before_request():
    """Connect to database before requests"""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close connection to database after requests"""
    g.db.close()
    return response

@app.route('/')
def index():
    return "Hi"

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit:
        flash("You've successfully registered, welcome to the ultimate taco website!", "success")
        models.User.create_user(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )
        return redirect(url_for('index'))
    return render_template('index.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():



if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='dtonlai',
            email='dtonlai@ualberta.ca',
            password='keyword',
            admin=True
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)