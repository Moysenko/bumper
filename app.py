from flask import Flask, request, render_template, redirect
from backend.feed_lib import Feed
from backend.console_interface_lib import Scanner

app = Flask(__name__)

admin = Scanner.get_creator('Admin')
feed = Feed(admin.id)


@app.route('/', methods=['GET'])
def get():
    return render_template('posts_grid.html', post_ids = feed.load_all_posts(True))


@app.route('/add_post', methods=['POST'])
def add_post():
    post_text = request.form['post_text']
    new_post = Scanner.get_post(author_id=admin.id,
                                raw_content_data=post_text.split('\r\n'))
    print(new_post.content.tiles)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
