from typing import List

from mmasters.config.database import db
from mmasters.entity.movie_snapshot import MovieSnapshotEntity, RatingEntity


class MovieSnapshotFixture:

    @staticmethod
    def save(movie_snapshot: MovieSnapshotEntity):
        db.session.add(movie_snapshot)
        db.session.commit()

    @staticmethod
    def find_all() -> List[MovieSnapshotEntity]:
        return MovieSnapshotEntity.query.all()

    @staticmethod
    def delete_all():
        RatingEntity.query.delete()
        MovieSnapshotEntity.query.delete()
