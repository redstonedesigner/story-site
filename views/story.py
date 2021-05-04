from flask import Blueprint, render_template, g, jsonify, redirect, request, abort
from models import Story, Category, User
from checks import login_required

story_bp = Blueprint(
    'stories',
    'stories',
    template_folder='templates/stories/',
    url_prefix='/stories'
)


@story_bp.route('/')
@login_required
def list_view():
    return render_template('story_all.html', g=g)


@story_bp.route('/all')
@login_required
def list_process():
    stories: list[Story] = Story.query.all()
    story_list = []
    for story in stories:
        story_categories = list(story.categories)
        story_category_slugs = []
        for category in story_categories:
            cat: Category = Category.query.filter(Category.id == category).first()
            if cat is None:
                return abort(500)
            story_category_slugs.append(cat.url_slug)
        author: User = User.query.filter(User.id == story.author).first()
        if author is None:
            return abort(500)
        data = {
            'title': story.title,
            'description': story.description,
            'categories': story_category_slugs,
            'url_slug': story.url_slug,
            'author': author.username
        }
        story_list.append(data)
    return jsonify(stories=story_list)


@story_bp.route('/<string:slug>')
@login_required
def single_view(slug):
    s: Story = Story.query.filter(Story.url_slug == slug).first()
    if s is None:
        return abort(404)
    return render_template('user_single.html', g=g, s=s)
