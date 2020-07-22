import idtype_lib


class Creator:
    def __init__(self, creator_id=None, face=None, name=None, subs=None, posts=None):
        self.face = face
        self.name = name
        self.id = creator_id
        self.subscriptions = subs if subs is not None else []
        self.posts = posts if posts is not None else []

    @staticmethod
    def create_creator(*args, **kwargs):
        new_creator = Creator(*args, **kwargs)
        if new_creator.id is None:
            new_creator.id = idtype_lib.CreatorId.save_to_database(new_creator)
        return new_creator
