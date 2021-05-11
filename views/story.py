from flask import Blueprint, render_template, g, jsonify, redirect, request, abort
from models import Story, Category, User, StoryCategory, Chapter
from checks import login_required
import utils


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
        categories: list[Category] = story.get_category_relations()
        author: User = story.get_author()
        data = {
            'title': story.title,
            'description': story.description,
            'categories': categories,
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


@story_bp.route('/<int:id>-json')
@login_required
def single_json(id):
    s: Story = Story.query.filter(Story.id == id).first()
    if s is None:
        return abort(404)
    categories = s.get_category_relations()
    chapters = []
    for i in s.chapters:
        chapters.append({
            "title": i.title,
            "id": i.id,
            "created_at": utils.format_date(i.created_at),
            "modified_at": utils.format_date(i.created_at)
        })
    story = {
        "title": s.title,
        "description": s.description,
        "categories": categories,
        "created": utils.format_date(s.created_at),
        "last_modified": utils.format_date(s.modified_at),
        "chapters": chapters,
        "author": s.get_author().username
    }
    return jsonify(story)
