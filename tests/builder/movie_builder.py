from typing import List

from mmasters.client.model.movie import Rating, Movie


class MovieBuilder:

    def __init__(self):
        self.__title = "Wanted"
        self.__release_year = "2008"
        self.__release_date = "27 June 2008"
        self.__director = "Timur Bekmambetov"
        self.__ratings = [Rating("Internet Movie Database", "6.7/10"), Rating("Rotten Tomatoes", "71%")]

    def with_title(self, title: str):
        self.__title = title
        return self

    def with_release_year(self, release_year: str):
        self.__release_year = release_year
        return self

    def with_release_date(self, release_date: str):
        self.__release_date = release_date
        return self

    def with_director(self, director: str):
        self.__director = director
        return self

    def with_ratings(self, ratings: List[Rating]):
        self.__ratings = ratings
        return self

    def build(self) -> Movie:
        return Movie(title=self.__title,
                     release_year=self.__release_year,
                     release_date=self.__release_date,
                     director=self.__director,
                     ratings=self.__ratings)
