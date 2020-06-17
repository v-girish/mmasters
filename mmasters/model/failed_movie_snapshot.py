from flask_restful import fields


class FailedMovieSnapshot:
    json_fields = {
        'title': fields.String,
    }

    @property
    def title(self): return self.__title

    def __init__(self, title: str):
        self.__title = title

    def __str__(self) -> str:
        return f"{{Title:{self.__title}}}"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.__title == other.__title