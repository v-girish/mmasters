from __future__ import annotations

from typing import List

from mmasters.client.model.movie import Movie
from mmasters.config.database import db
from mmasters.view.movie_snapshot_view import MovieSnapshotView
from mmasters.view.rating_view import RatingView


class MovieSnapshotEntity(db.Model):
    __tablename__ = 'movie_snapshots'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_year = db.Column(db.String)
    release_date = db.Column(db.String)
    director = db.Column(db.String)
    ratings: List[RatingEntity] = db.relationship('RatingEntity', backref=db.backref('movie_snapshot', lazy=True))

    @staticmethod
    def of(movie: Movie) -> MovieSnapshotEntity:
        ratings = [RatingEntity(source=rating.source, value=rating.value) for rating in movie.ratings]
        return MovieSnapshotEntity(title=movie.title,
                                   release_year=movie.release_year,
                                   release_date=movie.release_date,
                                   director=movie.director,
                                   ratings=ratings)

    def to_snapshot_view(self) -> MovieSnapshotView:
        ratings_view = [rating.to_snapshot_view() for rating in self.ratings]
        return MovieSnapshotView(self.id, self.title, self.release_year, self.release_date, self.director, ratings_view)


class RatingEntity(db.Model):
    __tablename__ = "ratings"
    ratings_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_snapshot_id = db.Column(db.Integer, db.ForeignKey('movie_snapshots.id'), nullable=False)
    source = db.Column(db.String)
    value = db.Column(db.String)

    def to_snapshot_view(self) -> RatingView:
        return RatingView(self.source, self.value)


