import logging
from typing import List, Union

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
        movie_snapshot_creation_response = MovieSnapshotCreationResponse()

        for title in titles:
            movie = movie_client.fetch(title)
            movie_snapshot_creation_response.add_snapshot(self.__save(movie))

        return movie_snapshot_creation_response

    def __save(self, movie: Movie) -> Union[SavedMovieSnapshot, FailedMovieSnapshot]:
        if movie.is_empty():
            return FailedMovieSnapshot(movie.title)

        movie_snapshot = movie_snapshot_repository.save(MovieSnapshotEntity.of(movie))
        return movie_snapshot.to_saved_snapshot()

    def get_all(self) -> List[MovieSnapshotView]:
        movie_snapshots = movie_snapshot_repository.find_all()
        self.logger.info(f"Fetched {len(movie_snapshots)} movie snapshots from database")
        return [movie_snapshot.to_snapshot_view() for movie_snapshot in movie_snapshots]


movie_snapshot_service = MovieSnapshotService()
