from unittest import TestCase
from unittest.mock import patch, call

from mmasters.entity.movie_snapshot import RatingEntity, MovieSnapshotEntity
from mmasters.exception.exception import MovieClientException
from mmasters.service.movie_snapshot_service import movie_snapshot_service
from mmasters.view.movie_snapshot_view import MovieSnapshotView
from mmasters.view.rating_view import RatingView
from mmasters.model.movie_snapshot_creation_response import MovieSnapshotCreationResponse, SavedMovieSnapshot, \
    FailedMovieSnapshot
from tests.builder.movie_builder import MovieBuilder


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

    def test_should_fetch_movies_from_movie_client(self):
        titles = ['Wanted', 'Dangal']

        movie_snapshot_service.create(titles)

        expected_calls = [call('Wanted'), call('Dangal')]
        self.movie_client.fetch.assert_has_calls(expected_calls, any_order=True)

    def test_should_save_two_movie_snapshots_returned_from_movie_client(self):
        titles = ['Wanted', 'Dangal']
        self.movie_client.fetch.side_effect = [MovieBuilder().build(), MovieBuilder().build()]
        self.movie_snapshot_repository.save.side_effect = [MovieSnapshotEntity(), MovieSnapshotEntity()]

        movie_snapshot_service.create(titles)

        self.assertEqual(2, self.movie_snapshot_repository.save.call_count)

    def test_should_return_movie_snapshot_creation_response_given_all_movies_are_saved_successfully(self):
        wanted_movie = MovieBuilder().with_title("Wanted").build()

        self.movie_client.fetch.side_effect = [wanted_movie]

        wanted_movie_snapshot = MovieSnapshotEntity(id=1, title="Wanted", release_year="2008",
                                                    release_date="27 June 2008", director="Timur Bekmambetov",
                                                    ratings=[
                                                        RatingEntity(source="Internet Movie Database", value="6.7/10"),
                                                        RatingEntity(source="Rotten Tomatoes", value="71%")])

        self.movie_snapshot_repository.save.side_effect = [wanted_movie_snapshot]

        movie_snapshot_creation_response = movie_snapshot_service.create(['Wanted'])

        expected_response = MovieSnapshotCreationResponse(saved_snapshots=[SavedMovieSnapshot(id=1, title="Wanted")])

        self.assertEqual(expected_response, movie_snapshot_creation_response)

    def test_should_return_movie_snapshot_creation_response_given_an_error_while_fetching_movie(self):
        self.movie_client.fetch.side_effect = MovieClientException("something went wrong")
        self.movie_snapshot_repository.save.return_value = None

        movie_snapshot_creation_response = movie_snapshot_service.create(['Wanted'])

        expected_response = MovieSnapshotCreationResponse(saved_snapshots=[],
                                                          failed_snapshots=[FailedMovieSnapshot("Wanted")])

        self.assertEqual(expected_response, movie_snapshot_creation_response)

    def test_should_return_movie_snapshot_creation_response_with_one_saved_snapshot_and_one_failed_snapshot(self):
        wanted_movie = MovieBuilder().with_title("Wanted").build()

        self.movie_client.fetch.side_effect = [wanted_movie, MovieClientException("something went wrong")]

        wanted_movie_snapshot = MovieSnapshotEntity(id=1, title="Wanted", release_year="2008",
                                                    release_date="27 June 2008", director="Timur Bekmambetov",
                                                    ratings=[
                                                        RatingEntity(source="Internet Movie Database", value="6.7/10"),
                                                        RatingEntity(source="Rotten Tomatoes", value="71%")])
        self.movie_snapshot_repository.save.side_effect = [wanted_movie_snapshot]

        movie_snapshot_creation_response = movie_snapshot_service.create(['Wanted', 'Dangal'])

        expected_response = MovieSnapshotCreationResponse(saved_snapshots=[SavedMovieSnapshot(id=1, title="Wanted")],
                                                          failed_snapshots=[FailedMovieSnapshot(title="Dangal")])

        self.assertEqual(expected_response, movie_snapshot_creation_response)

    def test_should_return_all_movie_snapshots(self):
        ratings = RatingEntity(source='Internet Movie Database', value='8.4/10')
        movie_snapshot = MovieSnapshotEntity(title="Dangal",
                                             id=1,
                                             release_year="2009",
                                             release_date='25 Dec 2009',
                                             director='Rajkumar Hirani',
                                             ratings=[ratings])
        self.movie_snapshot_repository.find_all.return_value = [movie_snapshot]

        actual_movie_snapshots = movie_snapshot_service.get_all()

        expected_movie_snapshots = [MovieSnapshotView(1, "Dangal", "2009", "25 Dec 2009", "Rajkumar Hirani",
                                                      ratings_view=[RatingView("Internet Movie Database", "8.4/10")])]

        self.assertEqual(expected_movie_snapshots, actual_movie_snapshots)
