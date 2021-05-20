from flask import Blueprint, render_template, g, jsonify, request, abort
from models import Category, StoryCategory, Story
from checks import login_required
from database import db_session

categories_bp = Blueprint(
	'categories',
	'categories',
	template_folder='templates/categories/',
	url_prefix='/categories'
)


@categories_bp.route('/')
@login_required
def list_view():
	return render_template('cat_list_multiple.html', g=g)


@categories_bp.route('/all')
@login_required
def list_process():
	categories = Category.query.all()
	category_list = []
	for category in categories:
		data = {
			'id': category.id,
			'name': category.name,
			'description': category.description,
			'url_slug': category.url_slug,
			'content_warning': category.content_warning
		}
		category_list.append(data)
	return jsonify(categories=category_list)


@categories_bp.route('/admin')
@login_required
def admin_view():
	if g.user.role != 2:
		return abort(403)
	return render_template('cat_admin.html')


@categories_bp.route('/delete', methods=['DELETE'])
@login_required
def admin_delete():
	if g.user.role != 2:
		return abort(403)
	category_id = request.form['category']
	category = Category.query.filter(Category.id == category_id).first()
	db_session.delete(category)
	db_session.commit()
	return "Success"


@categories_bp.route('/create', methods=['PUT'])
@login_required
def admin_create():
	if g.user.role != 2:
		return abort(403)
	name = request.form.get('name')
	url_slug = request.form.get('url_slug')
	description = request.form.get('description')
	content_warning = request.form.get('content_warning')
	errors = []
	if name == "":
		errors.append({
			"field": "name",
			"error": "Category name cannot be blank."
		})
	else:
		c_name_check = Category.query.filter(Category.name == name).first()
		if c_name_check is not None:
			errors.append({
				"field": "name",
				"error": "That name is already in use."
			})
	if url_slug == "":
		errors.append({
			"field": "url_slug",
			"error": "URL slug cannot be blank."
		})
	else:
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


@categories_bp.route('/id/<string:id>')
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


@categories_bp.route('/edit/<string:id>', methods=['PATCH'])
@login_required
def edit_process(id):
	if g.user.role != 2:
		return abort(403)
	name = request.form.get('name')
	url_slug = request.form.get('url_slug')
	description = request.form.get('description')
	content_warning = request.form.get('content_warning')
	errors = []
	if name == "":
		errors.append({
			"field": "name",
			"error": "Category name cannot be blank."
		})
	else:
		c_name_check = Category.query.filter(Category.name == name).first()
		if c_name_check is not None:
			if c_name_check.name != name:
				errors.append({
					"field": "name",
					"error": "That name is already in use."
				})
	if url_slug == "":
		errors.append({
			"field": "url_slug",
			"error": "URL slug cannot be blank."
		})
	else:
		c_slug_check = Category.query.filter(Category.url_slug == url_slug).first()
		if c_slug_check is not None:
			if c_slug_check.url_slug != url_slug:
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


@categories_bp.route('/<string:slug>')
@login_required
def single_view(slug):
	c = Category.query.filter(Category.url_slug == slug).first()
	if c is None:
		return abort(404)
	return render_template('cat_single.html', g=g, c=c)


@categories_bp.route('/<string:slug>-json')
@login_required
def single_json(slug):
	c = Category.query.filter(Category.url_slug == slug).first()
	if c is None:
		return abort(404)
	stories: list[Story] = [i.get_story() for i in StoryCategory.query.filter(StoryCategory.category_id == c.id).all()]
	stories_list = []
	for i in stories:
		data = {
			"title": i.title,
			"url_slug": i.url_slug,
			"description": i.description,
			"categories": i.get_category_relations(),
			"author": i.get_author().username
		}
		stories_list.append(data)
	category = {
		"name": c.name,
		"description": c.description,
		"url_slug": c.url_slug
	}
	return jsonify(stories=stories_list, category=category)