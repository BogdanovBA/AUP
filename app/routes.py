from app.forms import LoginForm, RegistrationForm, UpdateAccountForm, PasswordChangeForm
from flask import redirect, url_for, render_template, flash, request
from app import app, db
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
import secrets
import os


def save_picture(form_picture):
    random_hex = secrets.token_hex(8) 
    file_ext = form_picture.filename.split('.')[-1]
    picture_filename = random_hex + "." +  file_ext
    picture_path = os.path.join(app.root_path, 'static/media/' , picture_filename)
    form_picture.save(picture_path)

    return picture_filename


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm(obj=current_user)
    if request.method == 'POST' and not form.validate_on_submit():
        flash('Error while profile updating')
        return redirect(url_for('account'))
    if request.method == "POST" and form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data 
        current_user.email = form.email.data 
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('account'))

    image_file = url_for('static', filename='media/' + current_user.image_file)
    return render_template("account.html", image_file=image_file, form=form)



@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegistrationForm()
    if request.method =='POST' and not form.validate():
        flash('Invalid credentials. Try again')
        return redirect(url_for('register'))
    if request.method =='POST' and form.validate():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        logout_user()
        return redirect(url_for('login'))
    return render_template('logout.html')


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid credentials. Try again')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        flash(f'Successfully logged-in as { user.username }', 'success')
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('account')
        return redirect(next_page)
    return render_template("login.html", form=form)


@app.route('/password/change', methods=['GET', 'POST'])
@login_required
def password_change():
    form = PasswordChangeForm()
    if request.method == 'POST' and form.validate():
        if not current_user.check_password(form.old_password.data):
            flash('Old password is wrong')
            return redirect(url_for('password_change'))
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Password was changed')
        return redirect(url_for('password_changed'))
    return render_template('password.html', form=form)

@app.route('/password/change/done')
def password_changed():
    return render_template('password_changed.html')