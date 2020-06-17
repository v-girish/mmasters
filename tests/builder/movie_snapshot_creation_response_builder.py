from mmasters.model.failed_movie_snapshot import FailedMovieSnapshot
from mmasters.model.movie_snapshot_creation_response import MovieSnapshotCreationResponse
from mmasters.model.saved_movie_snapshot import SavedMovieSnapshot


class MovieSnapshotCreationResponseBuilder:
    def __init__(self):
        self.__saved_snapshots = []
        self.__failed_snapshots = []

    def add_saved_snapshot(self, saved_snapshot: SavedMovieSnapshot):
        self.__saved_snapshots.append(saved_snapshot)
        return self

    def add_failed_snapshot(self, failed_snapshot: FailedMovieSnapshot):
        self.__failed_snapshots.append(failed_snapshot)
        return self

    def build(self) -> MovieSnapshotCreationResponse:
        return MovieSnapshotCreationResponse(saved_snapshots=self.__saved_snapshots,
                                             failed_snapshots=self.__failed_snapshots)