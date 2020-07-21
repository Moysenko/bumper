class DataList:
    def __init__(self, data=None):
        self.data = data if data is not None else []

    def add_element(self, element):
        self.data.append(element)
        return len(self.data) - 1

    def get_element(self, element_id):
        if 0 <= element_id < len(self.data):
            return self.data[element_id]
        else:
            raise IndexError(f"There is no element in database with id = {element_id}")


class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class DataBase(Singleton):
    def __init__(self):
        data_types = ["creator", "post", "comment"]
        self.data = {data_type: DataList() for data_type in data_types}


data_base = DataBase()
