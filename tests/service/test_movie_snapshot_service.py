from unittest import TestCase
from unittest.mock import patch, call

from mmasters.entity.movie_snapshot import MovieSnapshot, Ratings
from mmasters.service.movie_snapshot_service import movie_snapshot_service
from mmasters.view.movie_snapshot_view import MovieSnapshotView, RatingView
from tests.builder import movies


class MovieSnapshotServiceTest(TestCase):

    def setUp(self) -> None:
        self.movie_snapshot_repository_patch = patch(
            "mmasters.service.movie_snapshot_service.movie_snapshot_repository")
        self.movie_snapshot_repository = self.movie_snapshot_repository_patch.start()

        self.movie_client_patch = patch('mmasters.service.movie_snapshot_service.movie_client')
        self.movie_client = self.movie_client_patch.start()

    def tearDown(self) -> None:
        self.movie_snapshot_repository_patch.stop()
        self.movie_client_patch.stop()

    def test_should_invoke_client_to_fetch_movies(self):
        titles = ['Wanted', 'Dangal']

        movie_snapshot_service.create(titles)

        expected_calls = [call('Wanted'), call('Dangal')]
        self.movie_client.fetch_movies.assert_has_calls(expected_calls, any_order=True)

    def test_save_two_movie_snapshots_of_movies_in_database(self):
        titles = ['Wanted', 'Dangal']
        self.movie_client.fetch_movies.side_effect = [movies.Wanted, movies.Dangal]
        self.movie_snapshot_repository.save.return_value = None

        movie_snapshot_service.create(titles)

        self.assertEqual(2, self.movie_snapshot_repository.save.call_count)

    def test_should_return_movie_snapshots_saved_in_database(self):
        titles = ['Wanted', 'Dangal']

        self.movie_client.fetch_movies.side_effect = [movies.Wanted, movies.Dangal]
        self.movie_snapshot_repository.save.return_value = None

        movie_snapshots = movie_snapshot_service.create(titles)

        wanted_movie_snapshot = MovieSnapshotView("Wanted", "2008", "27 June 2008", "Timur Bekmambetov",
                                                  ratings_view=[RatingView("Internet Movie Database", "6.7/10"),
                                                                RatingView("Rotten Tomatoes", "71%")])

        dangal_movie_snapshot = MovieSnapshotView("Dangal", "2009", "25 Dec 2009", "Rajkumar Hirani",
                                                  ratings_view=[RatingView("Internet Movie Database", "8.4/10"),
                                                                RatingView("Rotten Tomatoes", "100%")])
        self.assertEqual([wanted_movie_snapshot, dangal_movie_snapshot], movie_snapshots)
