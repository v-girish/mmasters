from typing import List, Union

from mmasters.client.model.movie import Movie, EmptyMovie
from mmasters.client.movie_client import movie_client
from mmasters.entity.movie_snapshot import MovieSnapshot
from mmasters.repository.movie_snapshot_repository import movie_snapshot_repository
from mmasters.view.movie_snapshot_view import MovieSnapshotView, EmptyMovieSnapshotView


class MovieSnapshotService:

    def create(self, titles: List[str]) -> List[MovieSnapshotView]:
        movie_snapshot_views = []
        for title in titles:
            movie = self.__fetch_movie(title)
            movie_snapshot_views.append(self.__save(movie))
        return movie_snapshot_views

    def __save(self, movie) -> MovieSnapshotView:
        if isinstance(movie, EmptyMovie) is True:
            return EmptyMovieSnapshotView(movie.title)

        movie_snapshot = MovieSnapshot.of(movie)
        movie_snapshot_repository.save(movie_snapshot)
        return movie_snapshot.to_snapshot_view()

    def __fetch_movie(self, title: str) -> Movie:
        try:
            return movie_client.fetch_movies(title)
        except Exception:
            return EmptyMovie(title)

    def get_all(self) -> List[MovieSnapshotView]:
        movie_snapshots = movie_snapshot_repository.find_all()
        return [movie_snapshot.to_snapshot_view() for movie_snapshot in movie_snapshots]


movie_snapshot_service = MovieSnapshotService()
