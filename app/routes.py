from app import app, db
from flask import render_template, url_for, redirect, request, flash
from app.forms import UserRegisterForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/home')
def home():
    return render_template('homepage.html')


@app.route('/accoubt')
@login_required
def account():
    return render_template('account.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = UserRegisterForm()
    if request.method == 'POST' and form.validate():
        user = User(
            username=form.username.data,
            email=form.email.data,
            )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Account successfully created.')
        return redirect(url_for('login'))
    return render_template(
        'register.html',
        form=form,
    ), flash('Invalid credentials while register.')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        return redirect(url_for('home'))
    return render_template('logout.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid credentials while login.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        flash('User successfully logged-in')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('home')
        return redirect(next_page)

    return render_template('login.html', form=form)
