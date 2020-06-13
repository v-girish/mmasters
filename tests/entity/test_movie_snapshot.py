from unittest import TestCase

from mmasters.client.model.movie import Rating
from mmasters.entity.movie_snapshot import MovieSnapshot
from tests.builder.movie_builder import MovieBuilder


class MovieSnapshotTest(TestCase):

    def test_should_create_movie_snapshot_with_title_from_a_movie(self):
        dangal_movie = MovieBuilder().with_title("Dangal").build()

        movie_snapshot = MovieSnapshot.of(dangal_movie)

        self.assertEqual("Dangal", movie_snapshot.title)

    def test_should_create_movie_snapshot_with_release_year_from_a_movie(self):
        dangal_movie = MovieBuilder().with_release_year("2009").build()

        movie_snapshot = MovieSnapshot.of(dangal_movie)

        self.assertEqual("2009", movie_snapshot.release_year)

    def test_should_create_movie_snapshot_with_release_date_from_a_movie(self):
        dangal_movie = MovieBuilder().with_release_date("25 Dec 2009").build()

        movie_snapshot = MovieSnapshot.of(dangal_movie)

        self.assertEqual("25 Dec 2009", movie_snapshot.release_date)

    def test_should_create_movie_snapshot_with_director_from_a_movie(self):
        dangal_movie = MovieBuilder().with_director("Rajkumar Hirani").build()

        movie_snapshot = MovieSnapshot.of(dangal_movie)

        self.assertEqual("Rajkumar Hirani", movie_snapshot.director)

    def test_should_create_movie_snapshot_with_ratings_source_from_a_movie(self):
        ratings = [Rating(source="some source", value="some value")]
        dangal_movie = MovieBuilder().with_ratings(ratings).build()

        movie_snapshot = MovieSnapshot.of(dangal_movie)

        self.assertEqual("some source", movie_snapshot.ratings[0].source)

    def test_should_create_movie_snapshot_with_ratings_value_from_a_movie(self):
        ratings = [Rating(source="some source", value="some value")]
        dangal_movie = MovieBuilder().with_ratings(ratings).build()

        movie_snapshot = MovieSnapshot.of(dangal_movie)

        self.assertEqual("some value", movie_snapshot.ratings[0].value)
