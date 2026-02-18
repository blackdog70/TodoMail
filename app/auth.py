from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
)
from werkzeug.security import check_password_hash, generate_password_hash
from .i18n import translate as _

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# Simple in-memory user store
# Each user maps to a dict with hashed password and basic profile info
users: dict[str, dict[str, str]] = {}

class User(UserMixin):
    def __init__(self, username: str):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users.get(username)
        if user and check_password_hash(user['password'], password):
            login_user(User(username))
            session['lang'] = user.get('language', 'en')
            return redirect(url_for('main.index'))
        flash(_('invalid_credentials'))
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        language = request.form.get('language', 'en')

        if username in users:
            flash(_('user_exists'))
        else:
            users[username] = {
                'password': generate_password_hash(password),
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'language': language,
            }
            login_user(User(username))
            session['lang'] = language
            return redirect(url_for('main.index'))
    return render_template('register.html')
