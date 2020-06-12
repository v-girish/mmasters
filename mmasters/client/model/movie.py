from mmasters.view.movie_snapshot_view import MovieSnapshotView


class Movie():
    def __init__(self, title, release_year):
        self.__title = title
        self.__release_year = release_year

    @property
    def title(self): return self.__title

    @property
    def release_year(self): return self.__release_year

    def to_snapshot_view(self):
        return MovieSnapshotView(self.__title, self.__release_year)