from flask import Blueprint, render_template, g, jsonify, redirect, request, abort
from models import User, UserProfile
from checks import login_required
from database import db_session
from hashlib import sha512, md5
from html import escape

users_bp = Blueprint(
    'users',
    'users',
    template_folder='templates/users/',
    url_prefix='/users'
)


@users_bp.before_request
def set_global_nav():
    g.category = "users"
    g.page = None


@users_bp.route('/')
@login_required
def list_view():
    return render_template('user_list_multiple.html', g=g)


@users_bp.route('/all')
@login_required
def list_process_restricted_data():
    users = User.query.all()
    user_list = []
    for user in users:
        data = {
            'id': user.id,
            'username': user.username,
            'role': user.role
        }
        user_list.append(data)
    return jsonify(users=user_list)


@users_bp.route('/admin-all')
@login_required
def list_process_all_data():
    if g.user.role != 2:
        return abort(403)
    users = User.query.all()
    user_list = []
    for user in users:
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
        user_list.append(data)
    return jsonify(users=user_list)


@users_bp.route('/admin')
@login_required
def admin_view():
    if g.user.role != 2:
        return abort(403)
    g.category = "users_admin"
    return render_template('user_admin.html')


@users_bp.route('/delete', methods=['DELETE'])
@login_required
def admin_delete():
    if g.user.role != 2:
        return abort(403)
    user_id = request.form['user']
    user = User.query.filter(User.id == user_id).first()
    db_session.delete(user)
    db_session.commit()
    return "Success"


@users_bp.route('/create', methods=['PUT'])
@login_required
def admin_create():
    if g.user.role != 2:
        return abort(403)
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    errors = []
    if username == "":
        errors.append({
            "field": "username",
            "error": "Username cannot be blank."
        })
    elif username in ['admin', 'list', 'mod', 'moderator', 'administrator', 'create', 'edit', 'id', 'update', 'get',
                      'view', 'settings']:
        errors.append({"field": "username", "error": "Username reserved due to system limitation."})
    else:
        u_name_check = User.query.filter(User.username == username).first()
        if u_name_check is not None:
            errors.append({
                "field": "username",
                "error": "That name is already in use."
            })
    if email == "":
        errors.append({
            "field": "email",
            "error": "Email cannot be blank."
        })
    else:
        u_email_check = User.query.filter(User.email == email).first()
        if u_email_check is not None:
            errors.append({
                "field": "email",
                "error": "That email is already in use."
            })
    if password == "":
        errors.append({
            "field": "password",
            "error": "Password cannot be blank."
        })
    if errors:
        return jsonify(errors=errors, success=False)
    else:
        u = User(
            username=username,
            email=email,
            password=sha512(password.encode('utf-8')).hexdigest()
        )
        db_session.add(u)
        db_session.commit()
        up = UserProfile(id=u.id)
        db_session.add(up)
        db_session.commit()
        return jsonify(success=True)


@users_bp.route('/id/<string:id>')
@login_required
def get_by_id_process(id):
    if g.user.role != 2:
        return abort(403)
    u = User.query.filter(User.id == id).first()
    if u is None:
        return abort(404)
    return jsonify(
        username=u.username,
        email=u.email,
        id=u.id,
        role=u.role
    )


@users_bp.route('/edit/<string:id>', methods=['PATCH'])
@login_required
def edit_process(id):
    if g.user.role != 2:
        return abort(403)
    username = request.form.get('username')
    email = request.form.get('email')
    errors = []
    u_name_check = User.query.filter(User.username == username).first()
    if u_name_check is not None:
        if u_name_check.username != username:
            errors.append({
                "field": "username",
                "error": "That name is already in use."
            })
    u_email_check = User.query.filter(User.email == email).first()
    if u_email_check is not None:
        if u_email_check.email != email:
            errors.append({
                "field": "email",
                "error": "That email is already in use."
            })
    if username in ['admin', 'list', 'mod', 'moderator', 'administrator', 'create', 'edit', 'id', 'update', 'get',
                    'view', 'settings']:
        errors.append({"field": "username", "error": "Username reserved due to system limitation."})
    if errors:
        return jsonify(errors=errors, success=False)
    else:
        u = User.query.filter(User.id == id).first()
        u.username = username
        u.email = email
        db_session.commit()
        return jsonify(success=True)


@users_bp.route('/role/<int:id>', methods=["PATCH"])
@login_required
def set_role_process(id):
    if g.user.role != 2:
        return abort(403)
    u = User.query.filter(User.id == id).first()
    password = request.form.get('password')
    hashed_pw = sha512(password.encode('utf-8')).hexdigest()
    if g.user.password != hashed_pw:
        errors = [{
            "field": "password",
            "error": "Administrator password is incorrect."
        }]
        return jsonify(success=False, errors=errors)
    role = request.form.get('role')
    u.role = role
    db_session.commit()
    return jsonify(success=True)


@users_bp.route('/<string:username>')
@login_required
def single_view(username):
    u = User.query.filter(User.username == username).first()
    if u is None:
        return abort(404)
    return render_template('user_single.html', g=g, u=u)


@users_bp.route('/<string:username>-json')
@login_required
def single_json(username):
    u: User = User.query.filter(User.username == username).first()
    if u is None:
        return abort(404)
    email_hash = md5(g.user.email.encode('utf-8')).hexdigest()
    u_avatar_url = "https://www.gravatar.com/avatar/" + email_hash + ".jpg"
    profile: UserProfile = u.profile[0]
    user_details = {
        "username": u.username,
        "avatar": u_avatar_url,
        "following": u.get_following_count(),
        "followers": u.get_follower_count(),
        "about": {
            "education": profile.education,
            "location": profile.location,
            "skills": profile.skills,
            "notes": profile.notes
        }
    }
    return jsonify(user_details)


@users_bp.route('/settings')
@login_required
def user_settings_view():
    g.category = "user_settings"
    return render_template('user_settings.html')


@users_bp.route('/settings/profile', methods=['PATCH'])
def user_settings_edit_profile():
    up: UserProfile = g.user.profile[0]
    if up is None:
        return abort(500)
    up.education = escape(str(request.form.get('education')))
    up.skills = escape(str(request.form.get('skills')))
    up.location = escape(str(request.form.get('location')))
    up.notes = escape(str(request.form.get('notes')))
    db_session.commit()
    return jsonify(success=True)
