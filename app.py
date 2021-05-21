from flask import Flask, send_from_directory, render_template, g
from database import db_session
from views import auth, category, user, story, author
from checks import login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MJKDDHL73G8XbBGn2wdm2JsxWuaZUGtH'


@app.route('/')
@login_required
def hello_world():
    return render_template('index.html', g=g)


@app.route('/plugins/<path:path>')
def send_from_plugins(path):
    return send_from_directory('plugins', path)


@app.route('/dist/<path:path>')
def send_from_dist(path):
    return send_from_directory('dist', path)


app.register_blueprint(auth.auth_bp)
app.register_blueprint(category.categories_bp)
app.register_blueprint(user.users_bp)
app.register_blueprint(story.story_bp)
app.register_blueprint(author.author_bp)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.errorhandler(404)
@login_required
def error_404_handler(e):
    return render_template('404.html', g=g)


@app.errorhandler(500)
@login_required
def handle_500_error(e):
    return render_template('500.html', g=g)


@app.errorhandler(403)
@login_required
def handle_403_error(e):
    return render_template('403.html', g=g)


if __name__ == '__main__':
    app.run(debug=True)
