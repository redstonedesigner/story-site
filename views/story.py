from flask import Blueprint, render_template, g, jsonify, redirect, request, abort
from models import Story, Category, User, StoryCategory
from checks import login_required
from sqlalchemy import desc, asc

story_bp = Blueprint(
    'stories',
    'stories',
    template_folder='templates/stories/',
    url_prefix='/stories'
)


@story_bp.route('/')
@login_required
def list_view():
    return render_template('stories/story_recent.html', g=g)


@story_bp.route('/recent-json')
@login_required
def list_process():
    stories: list[Story] = Story.query.order_by(Story.modified_at.desc()).limit(10).all()
    story_list = []
    for story in stories:
        categories = StoryCategory.query.filter(StoryCategory.story_id == story.id).all()
        story_category_slugs = []
        for category_relation in categories:
            category: Category = Category.query.filter(category_relation.category_id == Category.id).first()
            story_category_slugs.append(category.url_slug)
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
    return render_template('story_single.html', g=g, s=s)
