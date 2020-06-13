from unittest import TestCase
from unittest.mock import patch, call

from mmasters.client.movie_client import MovieClient
from mmasters.service.movie_snapshot_service import movie_snapshot_service
from mmasters.view.movie_snapshot_view import MovieSnapshotView, RatingView
from tests.builder import movies


class MovieSnapshotServiceTest(TestCase):

    @patch('mmasters.service.movie_snapshot_service.movie_client')
    def test_should_invoke_client_to_fetch_movies(self, movie_client: MovieClient):
        titles = ['Wanted', 'Dangal']

        movie_snapshot_service.create(titles)

        expected_calls = [call('Wanted'), call('Dangal')]
        movie_client.fetch_movies.assert_has_calls(expected_calls, any_order=True)

    @patch('mmasters.service.movie_snapshot_service.movie_client')
    def test_should_return_movie_snapshots_fetched_from_client(self, movie_client: MovieClient):
        titles = ['Wanted', 'Dangal']

        movie_client.fetch_movies.side_effect = [movies.Wanted, movies.Dangal]

        movie_snapshots = movie_snapshot_service.create(titles)

        wanted_movie_snapshot = MovieSnapshotView("Wanted", "2008", "27 June 2008", "Timur Bekmambetov",
                                                  ratings_view=[RatingView("Internet Movie Database", "6.7/10"),
                                                                RatingView("Rotten Tomatoes", "71%")])

        dangal_movie_snapshot = MovieSnapshotView("Dangal", "2009", "25 Dec 2009", "Rajkumar Hirani",
                                                  ratings_view=[RatingView("Internet Movie Database", "8.4/10"),
                                                                RatingView("Rotten Tomatoes", "100%")])
        self.assertEqual([wanted_movie_snapshot, dangal_movie_snapshot], movie_snapshots)
