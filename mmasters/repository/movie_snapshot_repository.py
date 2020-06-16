from typing import List

from mmasters.config.database import db
from mmasters.entity.movie_snapshot import MovieSnapshotEntity


class MovieSnapshotRepository:
    def save(self, movie_snapshot: MovieSnapshotEntity) -> MovieSnapshotEntity:
        db.session.add(movie_snapshot)
        db.session.commit()
        return movie_snapshot

    def find_all(self) -> List[MovieSnapshotEntity]:
        return MovieSnapshotEntity.query.all()


movie_snapshot_repository = MovieSnapshotRepository()
