from typing import List

from mmasters.config.db_config import db
from mmasters.entity.movie_snapshot import MovieSnapshot


class MovieSnapshotRepository:
    def save(self, movie_snapshot: MovieSnapshot):
        db.session.add(movie_snapshot)
        db.session.commit()

    def find_all(self) -> List[MovieSnapshot]:
        return MovieSnapshot.query.all()


movie_snapshot_repository = MovieSnapshotRepository()
