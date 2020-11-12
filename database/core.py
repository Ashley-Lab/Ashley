import collections
import asyncio
import abc
from typing import overload, Type

from .cache import Cache
from .models import DatabaseModel, _SampleModel


class Database(abc.ABC):
    def __init__(self, models):
        self.models = models
        self.__cache = collections.defaultdict(Cache)

    def _transform_raw_data(self, data, from_):
        model = self.models.get(from_, _SampleModel)
        return model.from_dict(data, self)

    async def get_data(self, c, data_id):
        data = await self._get_cache_data(c, data_id)

        if not data:
            data = await self._get_raw_data(c, data_id)
            data = self._transform_raw_data(data, c)

        return data

    async def _get_cache_data(self, c, data_id):
        data = self.__cache[c][data_id]
        return await asyncio.sleep(0, result=data)

    @abc.abstractmethod
    async def _get_raw_data(self, c, data_id) -> dict:
        raise NotImplementedError()

    @overload
    async def _insert_into_cache(self, c, data: dict): -> Type[DatabaseModel]: ...
    @overload
    async def _insert_into_cache(self, c, data: Type[DatabaseModel]) -> None: ...
    async def _insert_into_cache(self, c, data):
        if type(data) is dict:
            data = self._transform_raw_data(data, c)
            return_data = None

        c = self.__cache[c]
        c.add(data)

        try: return_data
        except: return
        return data

    @abc.abstractmethod
    async def _insert_raw_data(self, c, data: dict):
        raise NotImplementedError()

    @overload
    async def insert_data(self, c, data: dict) -> Type[DatabaseModel]: ...
    @overload
    async def insert_data(self, c, data: Type[DatabaseModel]) -> None: ...
    async def insert_data(self, c, data):
        result = await self._insert_into_cache(c, data)
        data = data.to_dict() if result else data
        await self._insert_raw_data(c, data)
        return await asyncio.sleep(0, result=result)

    @overload
    async def _update_cache_data(self, c, data_id, new_data: dict) -> Type[DatabaseModel]: ...
    @overload
    async def _update_cache_data(self, c, data_id, new_data: Type[DatabaseModel]) -> None: ...
    async def _update_cache_data(self, c, data_id, new_data):
        c = self.__cache[c]
        del c[data_id]

        return_data = None
        if type(new_data) is dict:
            new_data = self._transform_raw_data(new_data, c)
            return_data = new_data

        c[data_id] = new_data

        return await asyncio.sleep(0, result=new_data)

    @abc.abstractmethod
    async def _update_raw_data(self, c, data_id, new_data: dict):
        raise NotImplementedError()

    @overload
    async def update_data(self, c, data_id, new_data: dict) -> Type[DatabaseModel]: ...
    @overload
    async def update_data(self, c, data_id, new_data: Type[DatabaseModel]) -> None: ...
    async def update_data(self, c, data_id, new_data):
        result = await self._update_cache_data(c, data_id, new_data)
        data = data.to_dict() if result else data
        await self._update_raw_data(c, data_id, new_data)
        return await asyncio.sleep(0, result=result)
