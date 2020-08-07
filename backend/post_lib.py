from . import content_lib
from . import comment_lib
from . import idtype_lib
import os


class Post:
    def __init__(self, record_information, title=None, content=None,
                 comments=None, post_id=None):
        self.title = title or ""
        self.record_information = record_information
        self.content = content or content_lib.Content()
        self.comments = comments or comment_lib.CommentSection()
        self.id = post_id

    def add_comment(self, comment):
        self.comments.add_comment(comment)

    @staticmethod
    def create_post(*args, **kwargs):
        new_post = Post(*args, **kwargs)
        if new_post.id is None:
            new_post.id = idtype_lib.PostId.save_to_database(new_post)
        new_post.record_information.author_id.instance().posts.append(new_post.id)
        return new_post

    def thumbnail(self):
        thumbnails_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                      os.pardir, 'static', 'thumbnails')

        allowed_image_formats = ['.jpg', '.png', '.jpeg']
        for ending in allowed_image_formats:
            filename = str(self.id.id) + ending
            absolute_filename = os.path.join(thumbnails_dir, filename)
            if os.path.isfile(absolute_filename):
                return os.path.join('static', 'thumbnails', filename)

        return None


