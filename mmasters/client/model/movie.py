from __future__ import annotations
from mmasters.view.movie_snapshot_view import MovieSnapshotView


class Movie():
    def __init__(self, title, release_year):
        self.__title = title
        self.__release_year = release_year

    @property
    def title(self) -> str: return self.__title

    @property
    def release_year(self) -> str: return self.__release_year

    def to_snapshot_view(self) -> MovieSnapshotView:
        return MovieSnapshotView(self.__title, self.__release_year)

    @classmethod
    def from_json(cls, json_response: dict) -> Movie:
        return Movie(json_response['Title'], json_response['Year'])

    def __eq__(self, other) -> bool:
        return self.__title == other.title and self.__release_year == other.release_year

