class Feed:
    def __init__(self, user_id):
        self.user_id = user_id

    def load_all_posts(self, list_all_internet=False):
        posts = []
        subs = self.user_id.instance().subs
        if list_all_internet:
            import idtype_lib
            subs = range(idtype_lib.CreatorId.max_id() + 1)
        for subsctiption in subs:
            posts += subsctiption.instance().posts
        posts.sort(key=lambda post_id: post_id.instance().record_information.date, reverse=True)
        return posts
