from __future__ import annotations
from typing import List

from flask_restful import fields


class MovieSnapshotView:

    def __init__(self, title: str, release_year: str, release_date: str, director: str, ratings_view: List[RatingView]):
        self.__title = title
        self.__release_year = release_year
        self.__release_date = release_date
        self.__director = director
        self.__ratings_view = ratings_view

    @property
    def title(self): return self.__title

    @property
    def release_year(self): return self.__release_year

    @property
    def release_date(self) -> str: return self.__release_date

    @property
    def director(self) -> str: return self.__director

    @property
    def ratings_view(self) -> List[RatingView]: return self.__ratings_view.copy()

    @property
    def is_empty(self): return False

    def __eq__(self, other):
        return self.title == other.title and \
               self.release_year == other.release_year and \
               self.release_date == other.release_date and \
               self.director == other.director and \
               self.ratings_view == other.ratings_view

    def __str__(self):
        return f"title:{self.title},release_year:{self.release_year},release_date:{self.release_date}," \
               f"director:{self.director},ratings_view:{self.ratings_view}"

    def __repr__(self):
        return self.__str__()


class RatingView:
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


class EmptyMovieSnapshotView(MovieSnapshotView):
    def __init__(self, title):
        super(EmptyMovieSnapshotView, self).__init__(title, "", "", "", [])

    @property
    def is_empty(self): return True


ratings_view_fields = {
    "source": fields.String,
    "value": fields.String
}

movie_snapshot_view_fields = {
    'title': fields.String,
    'releaseYear': fields.String(attribute="release_year"),
    'releaseDate': fields.String(attribute="release_date"),
    'director': fields.String,
    'is_empty': fields.Boolean,
    'ratings': fields.List(fields.Nested(ratings_view_fields), attribute="ratings_view")
}
