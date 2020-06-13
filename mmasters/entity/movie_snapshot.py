from __future__ import annotations

from mmasters.client.model.movie import Movie
from mmasters.config.db_config import db


class MovieSnapshot(db.Model):
    __tablename__ = 'movie_snapshots'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_year = db.Column(db.String)
    release_date = db.Column(db.String)
    director = db.Column(db.String)
    ratings = db.relationship('Ratings', backref=db.backref('movie_snapshot', lazy=True))

    @staticmethod
    def of(movie: Movie) -> MovieSnapshot:
        ratings = [Ratings(source=rating.source, value=rating.value) for rating in movie.ratings]
        return MovieSnapshot(title=movie.title,
                             release_year=movie.release_year,
                             release_date=movie.release_date,
                             director=movie.director,
                             ratings=ratings)


class Ratings(db.Model):
    __tablename__ = "ratings"
    ratings_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_snapshot_id = db.Column(db.Integer, db.ForeignKey('movie_snapshots.id'), nullable=False)
    source = db.Column(db.String)
    value = db.Column(db.String)


