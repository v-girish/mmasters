from __future__ import annotations
from typing import List, Union

from flask_restful import fields

from mmasters.model.failed_movie_snapshot import FailedMovieSnapshot
from mmasters.model.saved_movie_snapshot import SavedMovieSnapshot


class MovieSnapshotCreationResponse:
    json_fields = {
        'saved_snapshots': fields.List(fields.Nested(SavedMovieSnapshot.json_fields)),
        'failed_snapshots': fields.List(fields.Nested(FailedMovieSnapshot.json_fields))
    }

    def __init__(self,
                 saved_snapshots: List[SavedMovieSnapshot] = None,
                 failed_snapshots: List[FailedMovieSnapshot] = None):
        if failed_snapshots is None:
            failed_snapshots = []
        if saved_snapshots is None:
            saved_snapshots = []
        self.__saved_snapshots = saved_snapshots
        self.__failed_snapshots = failed_snapshots

    @property
    def saved_snapshots(self):
        return self.__saved_snapshots.copy()

    @property
    def failed_snapshots(self):
        return self.__failed_snapshots.copy()

    def __str__(self) -> str:
        return "{saved_snapshots:[" + ",".join(
            [str(saved_snapshot) for saved_snapshot in self.__saved_snapshots]) + "]" + \
               ",{failed_snapshots:[" + ",".join(
            [str(failed_snapshot) for failed_snapshot in self.__failed_snapshots]) + "]}"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.__saved_snapshots == other.__saved_snapshots and self.__failed_snapshots == other.__failed_snapshots

    def __add_failed_snapshot(self, failed_snapshot: FailedMovieSnapshot) -> None:
        self.__failed_snapshots.append(failed_snapshot)

    def __add_saved_snapshot(self, saved_snapshot: SavedMovieSnapshot):
        self.__saved_snapshots.append(saved_snapshot)

    def add_snapshot(self, movie_snapshot: Union[SavedMovieSnapshot, FailedMovieSnapshot]):
        if movie_snapshot.is_failed():
            self.__add_failed_snapshot(movie_snapshot)
        else:
            self.__add_saved_snapshot(movie_snapshot)
