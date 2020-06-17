import logging
from typing import List

from mmasters.client.model.movie import Movie, EmptyMovie
from mmasters.client.movie_client import movie_client
from mmasters.entity.movie_snapshot import MovieSnapshotEntity
from mmasters.repository.movie_snapshot_repository import movie_snapshot_repository
from mmasters.view.movie_snapshot_view import MovieSnapshotView
from mmasters.model.movie_snapshot_creation_response import SavedMovieSnapshot, MovieSnapshotCreationResponse, \
    FailedMovieSnapshot


class MovieSnapshotService:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create(self, titles: List[str]) -> MovieSnapshotCreationResponse:
        saved_snapshots = []
        failed_snapshots = []

        for title in titles:
            movie = self.__fetch_movie(title)
            if movie.is_empty():
                failed_snapshots.append(FailedMovieSnapshot(movie.title))
            else:
                saved_snapshots.append(self.__save(movie))

        return MovieSnapshotCreationResponse(saved_snapshots=saved_snapshots,
                                             failed_snapshots=failed_snapshots)

    def __save(self, movie) -> SavedMovieSnapshot:
        movie_snapshot = movie_snapshot_repository.save(MovieSnapshotEntity.of(movie))
        return movie_snapshot.to_saved_snapshot()

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
