import comment_lib
import idtype_lib
import post_lib
import content_lib
import record_information_lib
import feed_lib


class Scanner:
    @staticmethod
    def get_content():
        print('Что у вас нового?')
        content = content_lib.Content()

        is_typing = True
        while is_typing:
            content.add_tile(content_lib.Tile(input('> ')))
            is_typing = input('Желаете продолжить? (Д/н)').strip().lower() == 'д'

        return content

    @staticmethod
    def get_record_information(author_id):
        return record_information_lib.RecordInformation(idtype_lib.CreatorId(author_id))

    @staticmethod
    def get_post(author_id):
        record_info = Scanner.get_record_information(author_id)
        content = Scanner.get_content()
        return post_lib.Post.create_post(record_information=record_info, content=content)

    @staticmethod
    def get_comment(post_id, author_id, reply_to=None):
        record_info = Scanner.get_record_information(author_id)
        content = Scanner.get_content()
        if reply_to is not None:
            reply_to = idtype_lib.CommentId(reply_to)

        comment = comment_lib.Comment.create_comment(record_information=record_info,
                                                     content=content,
                                                     reply_to=reply_to)
        post_id.instance().add_comment(comment)


class Interface:
    @staticmethod
    def add_indent(string, number_of_indents, indent_length=4):
        indent = ' ' * (indent_length * number_of_indents)
        return '\n'.join([indent + line for line in string.split('\n')])

    @staticmethod
    def wrap(string):
        lines = string.split('\n')
        horizontal_length = max([len(line) for line in lines])
        wrapped_string = '╭' + '─' * horizontal_length + '╮' + '\n'
        for line in lines:
            wrapped_string += '│' + line + ' ' * (horizontal_length - len(line)) + '│\n'
        wrapped_string += '╰' + '─' * horizontal_length + '╯'
        return wrapped_string

    @staticmethod
    def content_to_text(content):
        return '\n'.join([str(tile.data) for tile in content.tiles])

    @staticmethod
    def add_record_info_to_content(obj):
        record_info = obj.record_information
        content = Interface.content_to_text(obj.content)

        result = f"Post id: {obj.id.id}, author: {record_info.author_id.instance().name}\n"
        result += content + '\n'
        result += f"posted on {record_info.date}"
        return result

    @staticmethod
    def comment_visualisation(comment):
        return Interface.wrap(Interface.add_record_info_to_content(comment))

    @staticmethod
    def comment_section_visualisation(comment_section):
        comments_grid = []
        children_dict = comment_section.to_defaultdict()

        def transform_to_comments_grid(current_comment_id, current_indent=0):
            if current_comment_id is not None:
                comments_grid.append(Interface.add_indent(Interface.visualisation(current_comment_id), current_indent))
            for reply_id in children_dict[current_comment_id]:
                transform_to_comments_grid(reply_id, current_indent + 1)

        transform_to_comments_grid(None)  # None is the root of the comments tree

        return Interface.wrap('\n'.join(comments_grid))

    @staticmethod
    def post_visualisation(post):
        return Interface.wrap(Interface.wrap(Interface.add_record_info_to_content(post)) +
                              '\n' + Interface.visualisation(post.comments))

    @staticmethod
    def visualisation(obj):
        function_selector = {idtype_lib.IdType: lambda obj_id: Interface.visualisation(obj_id.instance()),
                             comment_lib.Comment: Interface.comment_visualisation,
                             comment_lib.CommentSection: Interface.comment_section_visualisation,
                             post_lib.Post: Interface.post_visualisation}

        for typename, visualiser in function_selector:
            if isinstance(obj, typename):
                return visualiser(obj)

    @staticmethod
    def show_feed(user_id, list_all_internet=False):
        feed = feed_lib.Feed(user_id)
        result = list(map(lambda post: Interface.visualisation(post), feed.load_all_posts(list_all_internet)))
        separator = '\n' * 4
        return Interface.wrap(separator.join(result))
