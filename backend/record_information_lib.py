from time import gmtime, strftime


class RecordInformation:
    def __init__(self, author_id, date=strftime("%Y-%m-%d %H:%M:%S", gmtime()), votes_counter=0):
        self.author_id = author_id
        self.date = date
        self.votes_counter = votes_counter
