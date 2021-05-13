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


@story_bp.route('/<string:url_slug>-json')
@login_required
def single_json(url_slug):
    s: Story = Story.query.filter(Story.url_slug == url_slug).first()
    if s is None:
        return abort(404)
    categories = s.get_category_relations()
    story = {
        "title": s.title,
        "description": s.description,
        "categories": categories,
        "has_chapters": s.multiple_chapters,
        "created": utils.format_date(s.created_at),
        "last_modified": utils.format_date(s.modified_at),
        "author": s.get_author().username,
        "url_slug": s.url_slug
    }
    if s.multiple_chapters:
        chapters = []
        for i in s.chapters:
            chapters.append({
                "title": i.title,
                "id": i.id,
                "created_at": utils.format_date(i.created_at),
                "modified_at": utils.format_date(i.modified_at),
                "url_slug": i.url_slug
            })
        story['chapters'] = chapters
    else:
        story_content = s.chapters[0].content
        story['content'] = story_content
    return jsonify(story)


@story_bp.route('/<string:story_slug>/<string:chapter_slug>')
@login_required
def single_chapter_view(story_slug, chapter_slug):
    s: Story = Story.query.filter(Story.url_slug == story_slug).first()
    if s is None:
        return abort(404)
    c: Chapter = Chapter.query.filter(Chapter.url_slug == chapter_slug).first()
    if c is None:
        return abort(404)
    return render_template('story_chapter.html', g=g, s=s, c=c)


@story_bp.route('/<string:story_slug>/<string:category_slug>-json')
@login_required
def chapter_json(story_slug, category_slug):
    s: Story = Story.query.filter(Story.url_slug == story_slug).first()
    if s is None:
        return abort(404)
    c: Chapter = Chapter.query.filter(Chapter.url_slug == category_slug).first()
    if c is None:
        return abort(404)
    categories = s.get_category_relations()
    story = {
        "title": s.title,
        "description": s.description,
        "categories": categories,
        "has_chapters": s.multiple_chapters,
        "created": utils.format_date(s.created_at),
        "last_modified": utils.format_date(s.modified_at),
        "author": s.get_author().username,
        "url_slug": s.url_slug
    }
    chapter = {
        "title": c.title,
        "content": c.content,
        "created": utils.format_date(c.created_at),
        "last_modified": utils.format_date(c.modified_at),
    }
    c_index = s.chapters.index(c)
    if c_index + 1 < len(s.chapters):
        next_chapter: Chapter = s.chapters[c_index+1]
        chapter['next'] = next_chapter.url_slug
    if c_index != 0:
        prev_chapter: Chapter = s.chapters[c_index-1]
        chapter['prev'] = prev_chapter.url_slug
    return jsonify(story=story, chapter=chapter)
