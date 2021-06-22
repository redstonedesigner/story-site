from flask import Blueprint, render_template, g, session, request, redirect, escape
from flask.json import dumps
from models import User, UserProfile
import hashlib
from checks import no_login_required
from database import db_session


auth_bp = Blueprint('auth', 'auth', template_folder='templates/auth/',
                    url_prefix='/auth')


@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter(User.id == user_id).first()
        if g.user is None:
            session.clear()
            return redirect('/auth/login')
        email_hash = hashlib.md5(g.user.email.encode('utf-8')).hexdigest()
        g.avatar_url = "https://www.gravatar.com/avatar/" + email_hash + ".jpg"


@auth_bp.route('/login')
@no_login_required
def login_view():
    return render_template('login.html')


@auth_bp.route('/register')
@no_login_required
def register_view():
    return render_template('register.html')


@auth_bp.route('/login-process', methods=['POST'])
@no_login_required
def login_process():
    email = escape(request.form['email'])
    password = escape(request.form['password'])
    hashed_pw = hashlib.sha512(password.encode('utf-8')).hexdigest()
    user = User.query.filter(User.email == email).first()
    if user is None:
        return "Unauthorised"
    if user.password != hashed_pw:
        return "Unauthorised"
    else:
        session['user_id'] = user.id
        return "Authorised"


@auth_bp.route('/register-process', methods=['POST'])
@no_login_required
def register_process():
    email = escape(request.form['email'])
    username = escape(request.form['username'])
    password = escape(request.form['password'])
    password = hashlib.sha512(password.encode('utf-8')).hexdigest()
    password2 = escape(request.form['password2'])
    password2 = hashlib.sha512(password2.encode('utf-8')).hexdigest()
    errors = []
    u_email = User.query.filter(User.email == email).first()
    if u_email is not None:
        errors.append({"field": "email", "error": "Email already in use!"})
    u_username = User.query.filter(User.username == username).first()
    if u_username is not None:
        errors.append({"field": "username", "error": "Username already in use!"})
    if username in ['admin', 'list', 'mod', 'moderator', 'administrator', 'create', 'edit', 'id', 'update', 'get',
                    'view', 'settings']:
        errors.append({"field": "username", "error": "Username reserved due to system limitation."})
    if password != password2:
        errors.append({"field": "password", "error": "Passwords do not match!"})
    if errors:
        response = {
            "success": "false",
            "errors": errors
        }
        response = dumps(response)
        return response
    else:
        u = User(email=email, password=password, username=username)
        db_session.add(u)
        db_session.commit()
        up = UserProfile(u.id)
        db_session.add(up)
        db_session.commit()
        return '{"success": "true"}'


@auth_bp.route('/logout')
def logout_process():
    session.clear()
    return redirect('/')
