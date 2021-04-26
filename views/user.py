from flask import Blueprint, render_template, g, jsonify, redirect, request, abort
from models import User
from checks import login_required
from database import db_session

users_bp = Blueprint(
	'users',
	'users',
	template_folder='templates/users/',
	url_prefix='/users'
)


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
		return redirect('/')
	return render_template('user_admin.html')


@users_bp.route('/delete', methods=['DELETE'])
@login_required
def admin_delete():
	if g.user.role != 2:
		return redirect('/')
	category_id = request.form['category']
	category = Category.query.filter(Category.id == category_id).first()
	db_session.delete(category)
	db_session.commit()
	return "Success"


@users_bp.route('/create', methods=['PUT'])
@login_required
def admin_create():
	name = request.form.get('name')
	url_slug = request.form.get('url_slug')
	description = request.form.get('description')
	content_warning = request.form.get('content_warning')
	errors = []
	c_name_check = Category.query.filter(Category.name == name).first()
	if c_name_check is not None:
		errors.append({
			"field": "name",
			"error": "That name is already in use."
		})
	c_slug_check = Category.query.filter(Category.url_slug == url_slug).first()
	if c_slug_check is not None:
		errors.append({
			"field": "url_slug",
			"error": "That URL slug is already in use."
		})
	if errors:
		return jsonify(errors=errors, success=False)
	else:
		c = Category(
			name=name,
			description=description,
			url_slug=url_slug,
			content_warning=content_warning
		)
		db_session.add(c)
		db_session.commit()
		return jsonify(success=True)


@users_bp.route('/id/<string:id>')
@login_required
def get_by_id_process(id):
	c = Category.query.filter(Category.id == id).first()
	if c is None:
		return abort(404)
	return jsonify(
		name=c.name,
		content_warning=c.content_warning,
		id=c.id,
		description=c.description,
		url_slug=c.url_slug
	)


@users_bp.route('/edit/<string:id>', methods=['PATCH'])
@login_required
def edit_process(id):
	name = request.form.get('name')
	url_slug = request.form.get('url_slug')
	description = request.form.get('description')
	content_warning = request.form.get('content_warning')
	errors = []
	c_name_check = Category.query.filter(Category.name == name).first()
	if c_name_check is not None:
		if c_name_check.id != int(id):
			errors.append({
				"field": "name",
				"error": "That name is already in use."
			})
	c_slug_check = Category.query.filter(Category.url_slug == url_slug).first()
	if c_slug_check is not None:
		if c_slug_check.id != int(id):
			errors.append({
				"field": "url_slug",
				"error": "That URL slug is already in use."
			})
	if errors:
		return jsonify(errors=errors, success=False)
	else:
		c = Category.query.filter(Category.id == id).first()
		c.name = name
		c.url_slug = url_slug
		c.description = description
		c.content_warning = content_warning
		db_session.commit()
		return jsonify(success=True)


@users_bp.route('/<string:username>')
@login_required
def single_view(username):
	u = User.query.filter(User.username == username).first()
	if u is None:
		return abort(404)
	return render_template('user_single.html', g=g, u=u)
