from flask_restful import fields


class MovieSnapshotView:

    def __init__(self, title, release_year):
        self.__title = title
        self.__release_year = release_year

    @property
    def title(self): return self.__title

    @property
    def release_year(self): return self.__release_year


movie_snapshot_view_fields = {
    'title': fields.String,
    'releaseYear': fields.String(attribute="release_year")
}