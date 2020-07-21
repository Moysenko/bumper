import content_lib
import comment_lib
import idtype_lib


class Post:
    def __init__(self, record_information, content=content_lib.Content(),
                 comments=comment_lib.CommentSection(), post_id=None):
        self.record_information = record_information
        self.content = content
        self.comments = comments
        self.id = post_id

    def add_comment(self, comment):
        self.comments.add_comment(comment)

    @staticmethod
    def create_post(*args, **kwargs):
        new_post = Post(*args, **kwargs)
        if new_post.id is None:
            new_post.id = idtype_lib.IdType.save_to_database(new_post)
        return new_post
