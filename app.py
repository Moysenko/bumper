from flask import Flask, request, render_template, redirect, session, flash
from backend.feed_lib import Feed
from backend.console_interface_lib import Scanner
import os
from markupsafe import escape
from backend.idtype_lib import CreatorId
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

# Preparation
app = Flask(__name__)
app.secret_key = os.urandom(16)
login_manager = LoginManager()
login_manager.init_app(app)

admin = Scanner.get_creator(name='admin', password="admin")
feed = Feed(admin.id)

uploads_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           'static', 'thumbnails')


# Flask-Login requirement
@login_manager.user_loader
def load_user(user_id):
    return CreatorId(int(user_id)).instance()


# HTML PAGES
@app.route('/', methods=['GET'])
def index():
    return redirect('/feed')


@app.route('/feed', methods=['GET'])
def feed_page():
    return render_template('feed.html', post_ids = feed.load_all_posts(True))


@app.route('/profile', methods=['GET'])
@login_required
def profile_page():
    user = CreatorId.id_by_name(current_user.name).instance()
    return render_template('profile.html', post_ids=user.posts)


# ADD POST
@login_required
def new_post_from_request():
    post_text = request.form['post_text']
    thumbnail = request.files.get('thumbnail')

    new_post = Scanner.get_post(author_id=CreatorId.id_by_name(current_user.name),
                                title=request.form['title'],
                                raw_content_data=post_text.split('\r\n'))

    if thumbnail is not None:
        filename = str(new_post.id.id) + '.' + thumbnail.filename.split('.')[-1]
        thumbnail.save(os.path.join(uploads_dir, filename))


@app.route('/feed/add_post', methods=['POST'])
def feed_page__add_post():
    new_post_from_request()
    return redirect('/feed')


@app.route('/profile_page/add_post', methods=['POST'])
def profile_page__add_post():
    new_post_from_request()
    return redirect('/profile')


# AUTHORIZATION
@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/feed')

    user = Scanner.get_creator(name=request.form['username'],
                               password=request.form['password'])
    if user is None or not user.check_password(request.form['password']):
        flash('Invalid username or password')
        return redirect('/feed')

    login_user(user)

    return redirect('/feed')


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect('/feed')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
