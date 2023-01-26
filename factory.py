from typing import Generic, TypeVar

import importlib

T = TypeVar('T')

class BaseFactory(Generic[T]):
    _items: dict[str, T] = {}
    _mapping: dict = {}
    _module: str|list[str] = ''

    @classmethod
    def create(cls, name: str, kwords: dict = {}) -> T:
        if not name in cls._mapping:
            raise Exception(f"missing class mapping for {name}")

        if not name in cls._items:
            modules = [cls._module] if not isinstance(cls._module, list) else cls._module

            for m in modules:
                try:
                    cls._items[name] = getattr(importlib.import_module(m), cls._mapping[name])(**kwords)
                    break
                except:
                    continue

        return cls._items[name]
