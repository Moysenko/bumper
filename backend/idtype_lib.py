from . import database_lib


class IdType:
    type_name = None

    def __init__(self, instance_id):
        self.id = instance_id

    def instance(self):
        return database_lib.data_base.data[self.type_name][self.id]

    @classmethod
    def save_to_database(cls, obj):
        new_id = database_lib.data_base.data[cls.type_name].add_element(obj)
        return cls(new_id)

    @classmethod
    def max_id(cls):
        return len(database_lib.data_base.data[cls.type_name]) - 1

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class CreatorId(IdType):
    type_name = "creator"
    username_hashmap = {}

    @classmethod
    def save_to_database(cls, obj):
        if obj.name not in cls.username_hashmap:
            creator_id = super().save_to_database(obj)
            cls.username_hashmap[obj.name] = creator_id
        return cls.username_hashmap[obj.name]

    @classmethod
    def id_by_name(cls, name):
        return cls.username_hashmap[name]


class PostId(IdType):
    type_name = "post"

class CommentId(IdType):
    type_name = "comment"
