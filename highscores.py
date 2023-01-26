import base64, datetime, json
from typing import TypedDict

from container import AutoContainer

class ScoreItem(TypedDict):
    name: str
    score: int
    date: datetime.datetime

class HighScores(AutoContainer[ScoreItem]):
    _filename = 'scores.dat'

    @staticmethod
    def _parse_data(data: str) -> list[ScoreItem]:
        return json.loads(base64.b64decode(data))

    @staticmethod
    def _serialize_data() -> str:
        return base64.b64encode(json.dumps(HighScores._get_data()).encode('utf-8')).decode()

    @staticmethod
    def _create_item(name: str, score: int) -> ScoreItem:
        return {"name": name, "score": score, "date": datetime.datetime.now()}

    @staticmethod
    def _parse_item(item: ScoreItem) -> dict:
        return {"name": item['name'], "value": item['score']}
