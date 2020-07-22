import comment_lib
import idtype_lib
import post_lib
import content_lib
import record_information_lib
import feed_lib
import creator_lib
import database_lib


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
    def scan_type(typename, message):
        while True:
            try:
                if typename == bool:
                    user_input = input(message + "(Д/н)").strip().lower() == 'д'
                else:
                    user_input = typename(input(message))
                return user_input
            except ValueError:
                pass

    @staticmethod
    def get_record_information():
        author_id = Scanner.scan_type(int, "Ваш id: ")
        return record_information_lib.RecordInformation(idtype_lib.CreatorId(author_id))

    @staticmethod
    def get_post():
        record_info = Scanner.get_record_information()
        content = Scanner.get_content()
        print(f"id поста: {post_lib.Post.create_post(record_information=record_info, content=content).id.id}")

    @staticmethod
    def get_comment():
        post_id = Scanner.scan_type(int, "id поста, к которому вы хотите оставить комментарий:")
        reply_to = None
        if Scanner.scan_type(bool, "Желаете ответить кому-то?"):
            reply_to = Scanner.scan_type(int, "id комментария, которому вы хотите ответить:")

        record_info = Scanner.get_record_information()
        content = Scanner.get_content()

        if reply_to is not None:
            reply_to = idtype_lib.CommentId(reply_to)

        comment = comment_lib.Comment.create_comment(record_information=record_info,
                                                     content=content,
                                                     reply_to=reply_to)
        idtype_lib.PostId(post_id).instance().add_comment(comment)
        print(f"id комментария: {comment.id.id}")

    @staticmethod
    def get_creator():
        name = input("Ваше имя: ")
        print(f"Ваш id: {creator_lib.Creator.create_creator(name=name).id.id}")


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
    def add_record_info_to_content(obj, object_name="Post"):
        record_info = obj.record_information
        content = Interface.content_to_text(obj.content)

        result = f"{object_name} id: {obj.id.id}, author: {record_info.author_id.instance().name}\n"
        result += content + '\n'
        result += f"posted on {record_info.date}"
        return result

    @staticmethod
    def comment_visualisation(comment):
        return Interface.wrap(Interface.add_record_info_to_content(comment, "Comment"))

    @staticmethod
    def comment_section_visualisation(comment_section):
        if comment_section.is_empty():
            return Interface.wrap('Комментарии отсутствуют\nНапишите первым!')

        comments_grid = ['Комментарии:']
        children_dict = comment_section.to_defaultdict()
        print(children_dict)

        def transform_to_comments_grid(current_comment_id, current_indent=-1):
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

        for typename, visualiser in function_selector.items():
            if isinstance(obj, typename):
                return visualiser(obj)

    @staticmethod
    def show_feed():
        user_id = Scanner.scan_type(int, "Ваш id:")
        list_all_internet = True

        feed = feed_lib.Feed(idtype_lib.CreatorId(user_id))
        for post_id in feed.load_all_posts(True):
            print(post_id.id, len(post_id.instance().comments))
        result = list(map(lambda post: Interface.visualisation(post), feed.load_all_posts(list_all_internet)))
        separator = '\n' * 4
        print(Interface.wrap(separator.join(result)))
