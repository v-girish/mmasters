from __future__ import annotations

from typing import List


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

    def __str__(self):
        return f"title:{self.title},release_year:{self.release_year},release_date:{self.release_date}," \
               f"director:{self.director},ratings:{self.ratings}"

    def __repr__(self):
        return self.__str__()

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

    def __str__(self):
        return f"source:{self.source},value:{self.value}"

    def __repr__(self):
        return self.__str__()


class EmptyMovie(Movie):
    def __init__(self, title: str):
        super().__init__(title, "", "", "", [])
