from typing import List

from mmasters.config.db_config import db
from mmasters.entity.movie_snapshot import MovieSnapshotEntity


class MovieSnapshotRepository:
    def save(self, movie_snapshot: MovieSnapshotEntity):
        db.session.add(movie_snapshot)
        db.session.commit()

    def find_all(self) -> List[MovieSnapshotEntity]:
        return MovieSnapshotEntity.query.all()


movie_snapshot_repository = MovieSnapshotRepository()
