from container import AutoContainer
from selector import BaseSelector, SelectorFactory

import json, os
from typing import Any, Iterator


def GetThemes(location: str = '', extension: str = '') -> Iterator[str]:
    for f in os.listdir(os.path.curdir + location):
        if len(extension) and f.endswith(f".{extension}"):
            yield f

class AppSettings(AutoContainer[BaseSelector]):
    _filename: str = 'settings.json'
    _data: list[dict[str, BaseSelector]] = []

    _defaults: list[dict[str, BaseSelector]] = [{
        "theme": SelectorFactory.create('str', {"items": [*GetThemes('/assets/', 'theme')]}),
        "sound": SelectorFactory.create('bool')
    }]

    @staticmethod
    def _parse_data(data: str):
        return [{k: SelectorFactory.create(type(v))} for k, v in json.loads(data)]

    @staticmethod
    def _serialize_data() -> str:
        return json.dumps(AppSettings._get_data())

    @staticmethod
    def _create_item(name: str, value: Any) -> dict:
        return {"name": name, "value": value}
