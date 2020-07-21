import console_interface_lib

options = ['write comment', 'create post', 'show feed']


def choose_option():
    choice = None
    while choice is None:
        print("Select one of the options:")
        print(' '.join(f"{number}) {option}" for number, option in enumerate(options)))
        try:
            choice = int(input())
        except ValueError:
            choice = None
    return choice

