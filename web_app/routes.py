from flask import request
from datetime import datetime, timezone

from flask_login import logout_user, login_required
from flask import flash, redirect, url_for
from flask_login import current_user, login_user
import sqlalchemy as sa
from web_app import app, db
from web_app.models import User, RegistrationForm
from flask import render_template, flash
from web_app.forms import LoginForm, EditProfileForm, EditWeatherLocationForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/weather')
@login_required
def weather():
    is_on_weather = True
    return render_template('weather.html',
                           weather=is_on_weather)


@app.route('/edit_weather', methods=['GET', 'POST'])
@login_required
def edit_weather():
    form = EditWeatherLocationForm()
    is_on_weather = True
    if form.validate_on_submit():
        current_user.location = form.location.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_weather'))
    elif request.method == 'GET':
        form.location.data = current_user.location
    return render_template('edit_profile.html',
                           title='Edit Weather Location',
                           form=form, weather=is_on_weather)


@app.route('/stock')
@login_required
def stock():
    """
    stocks = db.session.execute(
        sa.select(User.stocks).where(User.id == current_user.id)
    )
    """
    return render_template('stock.html')


@app.route('/crypto')
@login_required
def crypto():
    return render_template('crypto.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/profile/<username>')
@login_required
def profile(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    stocks = [
        {'name': 'AAPL', 'price': '100'},
        {'name': 'GOOG', 'price': '200'},
        {'name': 'MSFT', 'price': '300'},
    ]
    return render_template('profile.html', user=user, stocks=stocks)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    edit = True
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',
                           title='Edit Profile',
                           form=form, edit=edit)
