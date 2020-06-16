import logging
from typing import List

from mmasters.client.model.movie import Movie, EmptyMovie
from mmasters.client.movie_client import movie_client
from mmasters.entity.movie_snapshot import MovieSnapshotEntity
from mmasters.repository.movie_snapshot_repository import movie_snapshot_repository
from mmasters.view.movie_snapshot_view import MovieSnapshotView, EmptyMovieSnapshotView, AbstractMovieSnapshotView


class MovieSnapshotService:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create(self, titles: List[str]) -> List[AbstractMovieSnapshotView]:
        movie_snapshot_views = []
        for title in titles:
            movie = self.__fetch_movie(title)
            movie_snapshot_views.append(self.__save(movie))
        return movie_snapshot_views

    def __save(self, movie) -> AbstractMovieSnapshotView:
        if isinstance(movie, EmptyMovie) is True:
            return EmptyMovieSnapshotView(movie.title)

        movie_snapshot = MovieSnapshotEntity.of(movie)
        saved_movie_snapshot = movie_snapshot_repository.save(movie_snapshot)
        return saved_movie_snapshot.to_snapshot_view()

    def __fetch_movie(self, title: str) -> Movie:
        try:
            return movie_client.fetch(title)
        except Exception:
            self.logger.exception(f"Error while fetching movie with title {title}")
            return EmptyMovie(title)

    def get_all(self) -> List[MovieSnapshotView]:
        movie_snapshots = movie_snapshot_repository.find_all()
        self.logger.info(f"Fetched {len(movie_snapshots)} movie snapshots from database")
        return [movie_snapshot.to_snapshot_view() for movie_snapshot in movie_snapshots]


movie_snapshot_service = MovieSnapshotService()
