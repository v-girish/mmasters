from flask_restful import fields


class RatingView:
    ratings_view_fields = {
        "source": fields.String,
        "value": fields.String
    }

    def __init__(self, source: str, value: str):
        self.__source = source
        self.__value = value

    @property
    def source(self) -> str: return self.__source

    @property
    def value(self) -> str: return self.__value

    def __eq__(self, other) -> bool:
        return self.source == other.source and self.value == other.value

    def __str__(self):
        return f"source:{self.source},value:{self.value}"

    def __repr__(self):
        return self.__str__()