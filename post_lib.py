import content_lib
import comment_lib
import idtype_lib


class Post:
    def __init__(self, record_information, content=None,
                 comments=None, post_id=None):
        self.record_information = record_information
        self.content = content if content is not None else content_lib.Content()
        self.comments = comments if comments is not None else comment_lib.CommentSection()
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
