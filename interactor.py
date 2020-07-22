import console_interface_lib

options = {'Зарегистрироваться': console_interface_lib.Scanner.get_creator,
           'Написать комментарий': console_interface_lib.Scanner.get_comment,
           'Создать пост': console_interface_lib.Scanner.get_post,
           'Показать ленту': console_interface_lib.Interface.show_feed,
           'Выйти': None}


def choose_option():
    choice = None
    while choice is None:
        print("Выберите одну из опций:")
        print(';  '.join(f"{number}) {option}" for number, option in enumerate(options.keys())))
        try:
            choice = int(input())
            if not (0 <= choice < len(options)):
                choice = None
        except ValueError:
            choice = None
    return list(options.keys())[choice]


def interact():
    is_stopped = False
    while not is_stopped:
        choice = choose_option()
        if options[choice] is None:
            is_stopped = True
        else:
            options[choice]()


interact()