from unittest import TestCase

from mmasters.app import Application
from mmasters.entity.movie_snapshot import MovieSnapshot, Rating
from mmasters.repository.movie_snapshot_repository import MovieSnapshotRepository, movie_snapshot_repository
from tests.config.test_config import TestConfig


class MovieSnapshotRepositoryIntegrationTest(TestCase):

    def setUp(self) -> None:
        self.app = Application.create_app(TestConfig)
        self.app.app_context().push()
        Rating.query.delete()
        MovieSnapshot.query.delete()

    def test_should_store_movie_snapshots(self):
        ratings = Rating(source='Internet Movie Database', value='8.4/10')
        movie_snapshot_repository.save(MovieSnapshot(title="3 Idiots",
                                                     release_year="2009",
                                                     release_date='25 Dec 2009',
                                                     director='Rajkumar Hirani',
                                                     ratings=[ratings]))
        saved_movie_snapshots = MovieSnapshot.query.all()
        self.assertEqual(1, len(saved_movie_snapshots))

    def test_should_return_list_of_movie_snapshots_present_in_database(self):
        ratings = Rating(source='Internet Movie Database', value='8.4/10')
        movie_snapshot = MovieSnapshot(title="3 Idiots",
                                       release_year="2009",
                                       release_date='25 Dec 2009',
                                       director='Rajkumar Hirani',
                                       ratings=[ratings])
        MovieSnapshotRepository().save(movie_snapshot)
        saved_movie_snapshots = movie_snapshot_repository.find_all()

        expected_movie_snapshots = [movie_snapshot]

        self.assertEqual(expected_movie_snapshots, saved_movie_snapshots)
