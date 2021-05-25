from flask import Blueprint, render_template, g, jsonify, redirect, request, abort
from models import Story, Category, User, Chapter
from checks import login_required
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


@author_bp.route('/new')
@login_required
def author_new_story_view():
    return render_template('author_new_story.html', g=g)


@author_bp.route('/edit/<string:url_slug>')
@login_required
def author_edit_story_view(url_slug):
    return render_template('author_edit_story.html', g=g)


@author_bp.route('/new/<string:url_slug>')
@login_required
def author_new_chapter_view(url_slug):
    return render_template('author_new_chapter.html', g=g)


@author_bp.route('/edit/<string:story_slug>/<string:chapter_slug>')
@login_required
def author_edit_chapter_view(story_slug, chapter_slug):
    return render_template('author_edit_chapter.html', g=g)