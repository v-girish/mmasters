from typing import List

from mmasters.client.movie_client import movie_client
from mmasters.entity.movie_snapshot import MovieSnapshot
from mmasters.repository.movie_snapshot_repository import movie_snapshot_repository


class MovieSnapshotService:

    def create(self, titles: List[str]):
        movies = [movie_client.fetch_movies(title) for title in titles]
        for movie in movies:
            movie_snapshot_repository.save(MovieSnapshot.of(movie))
        return list(map(lambda _movie: _movie.to_snapshot_view(), movies))

    def get_all(self):
        movie_snapshots = movie_snapshot_repository.find_all()
        return [movie_snapshot.to_snapshot_view() for movie_snapshot in movie_snapshots]


movie_snapshot_service = MovieSnapshotService()
