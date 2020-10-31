from . import idtype_lib
from . import post_lib
import os


class Creator:
    def __init__(self, creator_id=None, face=None, name=None, password=None, subs=None, posts=None, info_line=None):
        self.face = face
        self.name = name
        self.id = creator_id
        self.subscriptions = subs or []
        self.posts = posts or []
        self.password = password
        self.info_line = info_line or ""

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

    def icon(self):
        user_icon = self.id.icon(os.path.join('user_files', 'icons'))
        return user_icon or os.path.join('user_files', 'icons', 'duck.jpg')
