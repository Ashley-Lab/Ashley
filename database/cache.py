import collections


class Cache(collections.OrderedDict):
    def __init__(self, limit: int = None):
        super().__init__()

        self.limit = limit if limit is not None else -1

    def __setitem__(self, *args):
        item_poped = None
        if len(self) == self.limit:
            item_poped = self.popitem(last=False)

        super().__setitem__(*args)
        return item_poped

    def add(self, name, value):
        return self.__setitem__(name, value)

    def remove(self, key):
        del self[key]
