import feed_lib


class Page:
    def __init__(self, user_id):
        self.user_id = user_id
        self.feed = feed_lib.Feed(user_id)


class Wall(Page):
    pass


class UserFeed(Page):
    pass
