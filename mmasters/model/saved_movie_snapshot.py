from flask_restful import fields


class SavedMovieSnapshot:
    json_fields = {
        'title': fields.String,
        'id': fields.Integer,
    }

    def __init__(self, id: int, title: str):
        self.__id = id
        self.__title = title

    @property
    def id(self): return self.__id

    @property
    def title(self): return self.__title

    def is_failed(self) -> bool: return False

    def __str__(self) -> str:
        return f"{{Id: {self.__id}, Title:{self.__title}}}"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.__id == other.__id and self.__title == other.__title