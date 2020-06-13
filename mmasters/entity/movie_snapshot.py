from __future__ import annotations

from typing import List

from mmasters.client.model.movie import Movie
from mmasters.config.db_config import db
from mmasters.view.movie_snapshot_view import MovieSnapshotView, RatingView


class MovieSnapshot(db.Model):
    __tablename__ = 'movie_snapshots'
    title = db.Column(db.String, primary_key=True)
    release_year = db.Column(db.String)
    release_date = db.Column(db.String)
    director = db.Column(db.String)
    ratings: List[Rating] = db.relationship('Rating',
                                            backref=db.backref('movie_snapshot', lazy=True))

    @staticmethod
    def of(movie: Movie) -> MovieSnapshot:
        ratings = [Rating(source=rating.source, value=rating.value) for rating in movie.ratings]
        return MovieSnapshot(title=movie.title,
                             release_year=movie.release_year,
                             release_date=movie.release_date,
                             director=movie.director,
                             ratings=ratings)

    def to_snapshot_view(self) -> MovieSnapshotView:
        ratings_view = [rating.to_snapshot_view() for rating in self.ratings]
        return MovieSnapshotView(self.title, self.release_year, self.release_date, self.director, ratings_view)


class Rating(db.Model):
    __tablename__ = "ratings"
    ratings_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_snapshot_title = db.Column(db.String, db.ForeignKey('movie_snapshots.title'), nullable=False)
    source = db.Column(db.String)
    value = db.Column(db.String)

    def to_snapshot_view(self) -> RatingView:
        return RatingView(self.source, self.value)


