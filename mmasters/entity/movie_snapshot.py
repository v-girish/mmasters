from mmasters.app import db


class MovieSnapshot(db.Model):
    __tablename__ = 'movie_snapshots'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_year = db.Column(db.String)
    release_date = db.Column(db.String)
    director = db.Column(db.String)
    ratings = db.relationship('Ratings', backref=db.backref('movie_snapshot', lazy=True))


class Ratings(db.Model):
    __tablename__ = "ratings"
    ratings_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_snapshot_id = db.Column(db.Integer, db.ForeignKey('movie_snapshots.id'), nullable=False)
    source = db.Column(db.String)
    value = db.Column(db.String)


