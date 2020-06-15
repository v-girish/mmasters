from typing import List

from mmasters.config.db_config import db
from mmasters.entity.movie_snapshot import MovieSnapshot, Rating


class MovieSnapshotFixture:

    @staticmethod
    def save(movie_snapshot: MovieSnapshot):
        db.session.add(movie_snapshot)
        db.session.commit()

    @staticmethod
    def find_all() -> List[MovieSnapshot]:
        return MovieSnapshot.query.all()

    @staticmethod
    def delete_all():
        Rating.query.delete()
        MovieSnapshot.query.delete()
