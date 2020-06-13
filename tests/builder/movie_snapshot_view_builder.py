from mmasters.view.movie_snapshot_view import RatingView, MovieSnapshotView


class MovieSnapshotViewBuilder:

    def __init__(self):
        self.__title = "Wanted"
        self.__release_year = "2008"
        self.__release_date = "27 June 2008"
        self.__director = "Timur Bekmambetov"
        self.__ratings_view = [RatingView("Internet Movie Database", "6.7/10"), RatingView("Rotten Tomatoes", "71%")]

    def with_title(self, title: str):
        self.__title = title
        return self

    def build(self) -> MovieSnapshotView:
        return MovieSnapshotView(title=self.__title,
                                 release_year=self.__release_year,
                                 release_date=self.__release_date,
                                 director=self.__director,
                                 ratings_view=self.__ratings_view)
