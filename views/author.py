from flask import Blueprint, render_template, g, jsonify, redirect, request, abort
from models import Story, Category, User, Chapter, StoryCategory
from checks import login_required
from database import db_session
import utils


author_bp = Blueprint(
    'authors',
    'authors',
    template_folder='templates/authors/',
    url_prefix='/authors'
)


@author_bp.before_request
def set_global_nav():
    g.category = "authors"
    g.page = None


@author_bp.route('/')
@login_required
def author_dashboard_view():
    return render_template('author_dashboard.html', g=g)


@author_bp.route('/<string:username>/stories-json')
@login_required
def author_story_list_process(username: str):
    u: User = User.query.filter(User.username == username).first()
    if u is None:
        return jsonify(success=False, error=404), 404
    stories = Story.query.filter(Story.author_id == u.id).all()
    story_list = []
    for story in stories:
        categories: list[Category] = story.get_category_relations()
        data = {
            'title': story.title,
            'description': story.description,
            'categories': categories,
            'url_slug': story.url_slug,
            'chapters': len(story.chapters),
            'is_multi_chapter': story.multiple_chapters
        }
        story_list.append(data)
    return jsonify(stories=story_list)


@author_bp.route('/new')
@login_required
def author_new_story_view():
    return render_template('author_new_story.html', g=g)


@author_bp.route('/new', methods=['PUT'])
def author_new_story_action():
    form = request.form
    categories = form.getlist('categories[]', int)
    title = form.get('title')
    description = form.get('description')
    if form.get('multiple_chapters') == 'true':
        multiple_chapters = True
    else:
        multiple_chapters = False
    story = Story(title=title, description=description, multiple_chapters=multiple_chapters, author=g.user)
    db_session.add(story)
    db_session.commit()
    for i in categories:
        sc = StoryCategory(story_id=story.id, category_id=i)
        db_session.add(sc)
    db_session.commit()
    return jsonify(success=True, slug=story.url_slug, multiple_chapters=story.multiple_chapters)


@author_bp.route('/edit/<string:url_slug>')
@login_required
def author_edit_story_view(url_slug):
    return render_template('author_edit_story.html', g=g, slug=url_slug)


@author_bp.route('/edit/<string:url_slug>', methods=['PATCH'])
@login_required
def author_edit_story_process(url_slug):
    s: Story = Story.query.filter(Story.url_slug == url_slug).first()
    if s is None:
        return abort(404)

    form = request.form
    categories = form.getlist('categories[]', int)
    title = form.get('title')
    description = form.get('description')
    if form.get('multiple_chapters') == 'true':
        multiple_chapters = True
    else:
        multiple_chapters = False

    s.title = title
    s.description = description
    s.multiple_chapters = multiple_chapters
    current_cats = s.get_category_relations()
    for i in current_cats:
        c = Category.query.filter(Category.url_slug == i['slug']).first()
        sc = StoryCategory.query.filter(StoryCategory.category_id == c.id and StoryCategory.story_id == s.id).first()
        db_session.delete(sc)
    for i in categories:
        sc = StoryCategory(story_id=s.id, category_id=i)
        db_session.add(sc)
    db_session.commit()
    return jsonify(success=True)


@author_bp.route('/new/<string:url_slug>')
@login_required
def author_new_chapter_view(url_slug):
    s = Story.query.filter(Story.url_slug == url_slug).first()
    if s is None:
        return abort(404)
    return render_template('author_new_chapter.html', g=g, s=s)


@author_bp.route('/new/<string:url_slug>', methods=['PUT'])
@login_required
def author_new_chapter_action(url_slug):
    s = Story.query.filter(Story.url_slug == url_slug).first()
    if s is None:
        return abort(404)

    form = request.form
    title = form.get('title')
    content: str = form.get('content')
    safe_content = content.replace('<script>', '<noscript>').replace('</script>', '</noscript>')

    ch = Chapter(story_id=s.id, title=title, content=safe_content)
    db_session.add(ch)
    db_session.commit()

    return jsonify(success=True)


@author_bp.route('/edit/<string:story_slug>/<string:chapter_slug>')
@login_required
def author_edit_chapter_view(story_slug, chapter_slug):
    return render_template('author_edit_chapter.html', g=g)