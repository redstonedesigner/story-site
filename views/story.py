from flask import Blueprint, render_template, g, jsonify, redirect, request, abort
from models import Story, Category, User, Chapter
from checks import login_required
import utils


story_bp = Blueprint(
    'stories',
    'stories',
    template_folder='templates/stories/',
    url_prefix='/stories'
)


@story_bp.before_request
def set_global_nav():
    g.category = "stories"
    g.page = None


@story_bp.route('/')
@login_required
def list_view():
    g.page = "stories_recent"
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
        try:
            story_content = s.chapters[0].content
        except IndexError:
            story_content = "This story has not been fully created yet.  Please check back soon."
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


@story_bp.route('/az')
@story_bp.route('/az/<string:letter>')
@login_required
def search_az_view(letter: str = ''):
    if len(letter) > 1:
        return abort(400)
    g.page = 'stories_az'
    if letter == '':
        return render_template('story_az_start.html', g=g)
    else:
        return render_template('story_az_results.html', g=g, l=letter)


@story_bp.route('/az/<string:letter>-json')
@login_required
def search_az_json(letter: str):
    if len(letter) != 1:
        return abort(400)
    stories: list[Story] = Story.query.filter(Story.title.startswith(letter.upper())).all()
    if letter == '0':
        for i in range(0, 9):
            stories.append(Story.query.filter(Story.title.startswith(str(i+1))).alll())
        stories.sort(key=lambda x: x.title)
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