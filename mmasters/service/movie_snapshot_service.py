from typing import List

from mmasters.client.movie_client import movie_client
from mmasters.entity.movie_snapshot import MovieSnapshot
from mmasters.repository.movie_snapshot_repository import movie_snapshot_repository
from mmasters.view.movie_snapshot_view import MovieSnapshotView


class MovieSnapshotService:

    def create(self, titles: List[str]) -> List[MovieSnapshotView]:
        movies = [movie_client.fetch_movies(title) for title in titles]

        def __save(movie) -> MovieSnapshotView:
            movie_snapshot = MovieSnapshot.of(movie)
            movie_snapshot_repository.save(movie_snapshot)
            return movie_snapshot.to_snapshot_view()

        return [__save(movie) for movie in movies]

    def get_all(self) -> List[MovieSnapshotView]:
        movie_snapshots = movie_snapshot_repository.find_all()
        return [movie_snapshot.to_snapshot_view() for movie_snapshot in movie_snapshots]


movie_snapshot_service = MovieSnapshotService()
