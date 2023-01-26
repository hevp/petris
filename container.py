from abc import ABC, abstractmethod
import copy, json
from typing import cast, Generic, Iterator, TypeVar

T = TypeVar('T')

class AutoContainer(ABC, Generic[T]):
    _filename: str
    _data: list[T] = []
    _defaults: list[T] = []

    @classmethod
    def __len__(cls) -> int:
        return len(cls._get_data())

    @classmethod
    def items(cls) -> Iterator[dict]:
        for i in cls._get_data():
            yield cls._parse_item(i)

    @classmethod
    def _get_data(cls) -> list[T]:
        if not len(cls._data):
            cls._load_data()
        return cls._data

    @abstractmethod
    def _parse_item(item: T) -> dict: ...

    @classmethod
    def all(cls) -> list[T]:
        return cls._get_data()

    @classmethod
    def _load_data(cls) -> bool:
        try:
            with open(cls._filename, 'r') as f:
                cls._data = cls._parse_data(f.read())
        except (IOError, json.JSONDecodeError, Exception) as e:
            print(f"error: {e}")
            cls._data = copy.copy(cls._defaults)
            return cls._store_data()

        return True

    @classmethod
    def _store_data(cls) -> bool:
        try:
            with open(cls._filename, 'w') as f:
                f.write(cls._serialize_data())
        except (IOError, Exception) as e:
            print(f"error: {e}")
            return False

        return True

    @classmethod
    def add_item(cls, **kwargs) -> bool:
        cls._data += [cls._create_item(**kwargs)]
        return cls._store_data()

    @staticmethod
    @abstractmethod
    def _create_item(**kwargs) -> T: ...

    @staticmethod
    @abstractmethod
    def _parse_data(data: str) -> list[T]: ...

    @staticmethod
    @abstractmethod
    def _serialize_data() -> str: ...
