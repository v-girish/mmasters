from unittest import TestCase
from unittest.mock import patch, call

from mmasters.client.model.movie import Movie
from mmasters.client.movie_client import MovieClient
from mmasters.service.movie_snapshot_service import movie_snapshot_service
from mmasters.view.movie_snapshot_view import MovieSnapshotView


class MovieSnapshotServiceTest(TestCase):

    @patch('mmasters.service.movie_snapshot_service.movie_client')
    def test_should_invoke_client_to_fetch_movies(self, movie_client: MovieClient):
        titles = ['3 Idiots', 'Dangal']

        movie_snapshot_service.create(titles)

        expected_calls = [call('3 Idiots'), call('Dangal')]
        movie_client.fetch_movies.assert_has_calls(expected_calls, any_order=True)

    @patch('mmasters.service.movie_snapshot_service.movie_client')
    def test_should_return_movie_snapshots_fetched_from_client(self, movie_client: MovieClient):
        titles = ['3 Idiots', 'Dangal']

        movie_client.fetch_movies.side_effect = [Movie("3 Idiots", "2009"), Movie("Dangal", "2019")]

        movie_snapshots = movie_snapshot_service.create(titles)

        self.assertEqual([MovieSnapshotView("3 Idiots", "2009"),
                          MovieSnapshotView("Dangal", "2019")], movie_snapshots)
