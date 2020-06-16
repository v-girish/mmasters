from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from flask_restful import fields, marshal

from mmasters.view.rating_view import RatingView


class AbstractMovieSnapshotView(ABC):

    def __init__(self, title: str):
        self.__title = title

    @property
    def title(self):
        return self.__title

    @abstractmethod
    def marshal(self):
        pass


class MovieSnapshotView(AbstractMovieSnapshotView):
    json_fields = {
        'title': fields.String,
        'id': fields.Integer(attribute='snapshot_id'),
        'releaseYear': fields.String(attribute="release_year"),
        'releaseDate': fields.String(attribute="release_date"),
        'director': fields.String,
        'is_empty': fields.Boolean,
        'ratings': fields.List(fields.Nested(RatingView.ratings_view_fields), attribute="ratings_view")
    }

    def __init__(self, snapshot_id: int, title: str, release_year: str, release_date: str, director: str,
                 ratings_view: List[RatingView]):
        super(MovieSnapshotView, self).__init__(title)
        self.__snapshot_id = snapshot_id
        self.__release_year = release_year
        self.__release_date = release_date
        self.__director = director
        self.__ratings_view = ratings_view

    @property
    def snapshot_id(self): return self.__snapshot_id

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

    def marshal(self):
        return marshal(self, MovieSnapshotView.json_fields)

    def __eq__(self, other):
        return self.title == other.title and \
               self.__snapshot_id == other.snapshot_id and \
               self.release_year == other.release_year and \
               self.release_date == other.release_date and \
               self.director == other.director and \
               self.ratings_view == other.ratings_view

    def __str__(self):
        return f"snapshot_id:{self.snapshot_id}, title:{self.title},release_year:{self.release_year},release_date:{self.release_date}," \
               f"director:{self.director},ratings_view:{self.ratings_view}"

    def __repr__(self):
        return self.__str__()


class EmptyMovieSnapshotView(AbstractMovieSnapshotView):
    json_fields = {
        'title': fields.String,
        'is_empty': fields.Boolean
    }

    def __init__(self, title):
        super(EmptyMovieSnapshotView, self).__init__(title)

    @property
    def is_empty(self): return True

    def __eq__(self, other) -> bool:
        return self.title == other.title

    def __str__(self):
        return f"title:{self.title}"

    def __repr__(self):
        return self.__str__()

    def marshal(self):
        return marshal(self, EmptyMovieSnapshotView.json_fields)
