from __future__ import annotations

from typing import List

from mmasters.view.movie_snapshot_view import MovieSnapshotView, RatingView


class Movie:
    def __init__(self, title: str, release_year: str, release_date: str, director: str, ratings: List[Rating]):
        self.__title = title
        self.__release_year = release_year
        self.__release_date = release_date
        self.__director = director
        self.__ratings = ratings

    @property
    def title(self) -> str: return self.__title

    @property
    def release_year(self) -> str: return self.__release_year

    @property
    def release_date(self) -> str: return self.__release_date

    @property
    def director(self) -> str: return self.__director

    @property
    def ratings(self) -> List[Rating]: return self.__ratings.copy()

    def to_snapshot_view(self) -> MovieSnapshotView:
        ratings_view = [rating.to_snapshot_view() for rating in self.__ratings]
        return MovieSnapshotView(self.__title, self.__release_year, self.__release_date, self.__director, ratings_view)

    @classmethod
    def from_json(cls, json_response: dict) -> Movie:
        ratings = [Rating.from_json(rating) for rating in json_response['Ratings']]
        return Movie(json_response['Title'], json_response['Year'],
                     json_response['Released'],
                     json_response['Director'],
                     ratings)

    def __eq__(self, other) -> bool:
        return self.title == other.title and \
               self.release_year == other.release_year and \
               self.release_date == other.release_date and \
               self.director == other.director and \
               self.ratings == other.ratings


class Rating:
    def __init__(self, source: str, value: str):
        self.__source = source
        self.__value = value

    @property
    def source(self) -> str: return self.__source

    @property
    def value(self) -> str: return self.__value

    def __eq__(self, other) -> bool:
        return self.source == other.source and self.value == other.value

    @classmethod
    def from_json(cls, json_response: dict) -> Rating:
        return Rating(json_response['Source'], json_response['Value'])

    def to_snapshot_view(self) -> RatingView:
        return RatingView(self.__source, self.__value)
