from flask import Flask, render_template, redirect, url_for, g, flash, abort
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

import forms
import models
import os

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = "asdjfoadsgugkgnigi090j3onfo3inojfojklsnl"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connect to database before requests"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    """Close connection to database after requests"""
    g.db.close()
    return response

@app.route('/')
def index():
    taco = models.Taco.select()
    return render_template("index.html", taco=taco)

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("You've successfully registered, welcome to the ultimate taco website!", "success")
        models.User.create_user(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Sorry, that email and password combination doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've successfully been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Sorry, that email and password combination doesn't match!", "error")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've successfully been logged out, see you next time!", "success")
    return redirect(url_for('login'))

@app.route('/taco', methods=('GET', 'POST'))
def taco():
    form = forms.TacoForm()
    if form.validate_on_submit():
        models.Taco.create(
            protein = form.protein.data.strip(),
            shell = form.shell.data.strip(),
            extras = form.extras.data.strip(),
            cheese = form.cheese.data,
            user = g.user._get_current_object()
        )
        flash("Taco created, thanks!", "success")
        return redirect(url_for("index"))
    return render_template("taco.html", form=form)

@app.route('/stream')
@app.route('/stream/<username>')
def stream(username=None):
    template = 'taco_stream.html'
    if username and username != current_user.username:
        try:
            user = models.User.select().where(
                models.User.username**username).get()
        except models.DoesNotExist:
            abort(404)
        else:
            stream = user.Taco.limit(100)
    else:
        stream = current_user.get_taco_stream().limit(100)
        user = current_user
    return render_template(template, stream=stream, user=user)

@app.route('/post/<int:post_id>')
@login_required
def view_taco(taco_id):
    taco = models.Taco.select().where(models.Taco.id == taco_id)
    return render_template('stream.html', stream=taco)

if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='test',
            email='test@example.com',
            password='password'
        )
    except ValueError:
        pass
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

