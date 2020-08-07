from . import idtype_lib
from . import post_lib


class Creator:
    def __init__(self, creator_id=None, face=None, name=None, password=None, subs=None, posts=None):
        self.face = face
        self.name = name
        self.id = creator_id
        self.subscriptions = subs if subs is not None else []
        self.posts = posts if posts is not None else []
        self.password = password

        # Flask-Login requirements
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return str(self.id.id)

    @staticmethod
    def create_creator(*args, **kwargs):
        # check whether user with such name already exists
        if 'name' in kwargs and idtype_lib.CreatorId.id_by_name(kwargs.get('name')) is not None:
            return idtype_lib.CreatorId.id_by_name(kwargs.get('name')).instance()

        new_creator = Creator(*args, **kwargs)
        if new_creator.id is None:
            new_creator.id = idtype_lib.CreatorId.save_to_database(new_creator)
        return new_creator

    def create_post(self, *args, **kwargs):
        new_post = post_lib.Post.create_post(*args, **kwargs)
        self.posts.append(new_post.id)

    def check_password(self, password):
        return self.password == password
