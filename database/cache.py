
import typing


class Cache:
    __slots__ = ("__data", "limit")

    def __init__(self, limit: int = None):
        self.__data = []
        self.limit = limit if limit is not None else -2

    def __iter__(self):
        return self.__data.__iter__()

    def clear(self):
        self.__data.clear()

    def replace(self, index: int, to: str):
        self.__data[index] = to

    def push(self, data: typing.Any):
        self.__data.append(data)
        if len(self.__data) + 1 == self.limit:
            return self.__data.pop()
