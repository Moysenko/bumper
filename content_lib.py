class Tile:
    def __init__(self, data):
        self.data = data


class Content:
    def __init__(self, tiles=None):
        self.tiles = tiles if tiles is not None else []

    def add_tile(self, tile):
        self.tiles.append(tile)

    def remove_tile(self, index):
        del self.tiles[index]

    def __getitem__(self, key):
        return self.tiles[key]