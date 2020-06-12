from typing import List

from mmasters.client.movie_client import movie_client


class MovieSnapshotService:

    def create(self, titles: List[str]):
        movies = [movie_client.fetch_movies(title) for title in titles]
        return list(map(lambda _movie: _movie.to_snapshot_view(), movies))


movie_snapshot_service = MovieSnapshotService()
