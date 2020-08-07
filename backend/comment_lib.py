from . import content_lib
from . import idtype_lib
from collections import defaultdict


class Comment:
    def __init__(self, record_information, comment_id=None, content=content_lib.Content(), reply_to=None):
        self.record_information = record_information
        self.id = comment_id
        self.content = content
        self.reply_to = reply_to

    @staticmethod
    def create_comment(*args, **kwargs):
        new_comment = Comment(*args, **kwargs)
        if new_comment.id is None:
            new_comment.id = idtype_lib.CommentId.save_to_database(new_comment)
        return new_comment


class CommentSection:
    def __init__(self, comments=None):
        self._comments = comments if comments is not None else []

    def add_comment(self, comment):
        print('COMMENT ADDED')
        if isinstance(comment, Comment):
            self._comments.append(comment.id)
        elif isinstance(comment, idtype_lib.CommentId):
            self._comments.append(comment)
        else:
            raise TypeError("Only object of Comment class or CommentId class can be added to CommentSection")

    def to_defaultdict(self):
        children_dict = defaultdict(list)

        for comment_id in self._comments:
            children_dict[comment_id.instance().reply_to].append(comment_id)

        for key in children_dict.keys():
            children_dict[key].sort(key=lambda reply_id: reply_id.instance().record_information.date)

        return children_dict

    def is_empty(self):
        return len(self._comments) == 0

    def __len__(self):
        return len(self._comments)

    def __iter__(self):
        for comment in self._comments:
            yield comment
