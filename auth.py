from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from users_policy import UsersPolicy
from models import User
import functools


bp = Blueprint('auth', __name__, url_prefix='/auth')


def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Для доступа к данной странице необходимо пройти процедуру аутентификации.'
    login_manager.login_message_category = 'warning'
    login_manager.user_loader(load_user)
    login_manager.init_app(app)


# class CurUser(UserMixin):
#     def __init__(self, user_id, login, role_id):
#         super().__init__()
#         self.id = user_id
#         self.login = login
#         self.role_id = role_id

#     @property
#     def is_admin(self):
#         return bp.config.get('ADMIN_ROLE_ID') == self.role_id

#     @property
#     def is_moder(self):
#         return bp.config.get('MODER_ROLE_ID') == self.role_id

#     def can(self, action, record=None):
#         users_policy = UsersPolicy(record=record)
#         method = getattr(users_policy, action, None)
#         if method is not None:
#             return method()
#         return False


def load_user(user_id):
    user = User.query.get(user_id)
    return user

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        if login and password:
            user = User.query.filter_by(login=login).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Вы успешно аутентифицированы.', 'success')
                next = request.args.get('next')
                return redirect(next or url_for('index'))
        flash('Введены неверные логин и/или пароль.', 'danger')
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

def check_rights(action):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.is_anonymous:
                flash('Авторизуйтесь для просмотра данной страницы!', 'danger')
                return redirect(url_for('index'))     
            elif not current_user.can(action):
                flash('У вас недостаточно прав для доступа к данной странице.', 'danger')
                return redirect(url_for('index'))     
            return func(*args, **kwargs)
        return wrapper           
    return decorator
