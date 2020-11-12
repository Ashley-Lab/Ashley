
import inspect

_PREFIX = "_db"


class DatabaseModel:
    def __init__(self, raw_data: dict, state):
        # Gera `KeyError` se `_id` não foi definido.
        self.define("_id", raw_data["_id"])
        self.state = state

    def define(self, name, value):
        name = _PREFIX + name
        self.__dict__[name] = value

    def get(self, name):
        name = _PREFIX + name
        return self.__dict__[name]

    @property
    def id(self):
        return self.get("_id")

    @classmethod
    def from_dict(cls, data: dict, state):
        return cls(data, state)

    def to_dict(self) -> dict:
        data = {}

        for name, member in inspect.getmembers(self):
            if name.startswith(_PREFIX):
                if member: # Calls `__bool__` of the object.
                    name = name[len(_PREFIX):]
                    data[name] = member

        return data


class _SampleModel:
    def __init__(self, raw_data: dict, state):
        cls = type(self)
        for k, v in raw_data.items():
            if type(v) is dict:
                raw_data[k] = cls(v)

        self.__dict__.update(raw_data)

    def __setattr__(self, name, value):
        if name not in self.__dict__:
            raise AttributeError("you can't define a new attribute")

        self.__dict__[name] = value

    def to_dict(self):
        return self.__dict__

    def __repr__(self) -> str:
        return f"<_SampleModel {self.__dict__!s}>"
