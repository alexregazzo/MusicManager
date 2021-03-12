from __future__ import annotations
from .track import Track
from .base import Base
from .exceptions import *
import typing
import spotify.hints
import utils

logger = utils.get_logger(__file__)


class History(Base):
    def __init__(self, *,
                 his_id: int,
                 use_username: int,
                 tra_id: int,
                 his_played_at: str):
        self.his_id = his_id
        self.use_username = use_username
        self.tra_id = tra_id
        self.his_played_at = his_played_at
        self._track = None

    @classmethod
    def create(cls, *,
               use_username: int,
               tra_id: int,
               his_played_at: str
               ) -> History:
        return cls.get(
            his_id=cls._insert(use_username=use_username,
                               tra_id=tra_id,
                               his_played_at=his_played_at))

    def __eq__(self, other: typing.Union[History, dict]):
        if type(other) is History:
            return other.use_username == self.use_username and other.his_played_at == self.his_played_at
        elif type(other) is dict:
            if "use_username" in other and "his_played_at" in other:
                return other["use_username"] == self.use_username and other["his_played_at"] == self.his_played_at

        raise NotComparableObjectsError()

    @property
    def track(self) -> Track:
        if self._track is None:
            self._track = Track.get(tra_id=self.tra_id)
        return self._track

    def json(self, *args) -> dict:
        addons = {
            "history_track": lambda: {"track": self.track}
        }
        jsonobj = {"his_id": self.his_id,
                   "use_username": self.use_username,
                   "tra_id": self.tra_id,
                   "his_played_at": self.his_played_at,
                   "json_arguments": list(addons.keys())}
        for arg in args:
            if arg in addons:
                jsonobj.update(addons[arg]())
        return jsonobj

    @classmethod
    def createMultipleRaw(cls, *, use_username: int, raw_histories: typing.List[spotify.hints.PlayHistory],
                          onExistRaiseError: bool = True) -> typing.List[History]:
        histories = History.getAll(use_username=use_username)
        results = []
        for raw_history in raw_histories:
            current_raw_history = {"use_username": use_username,
                                   "his_played_at": raw_history["played_at"],
                                   "tra_id": (raw_history["track"])["id"]}
            try:
                index = histories.index(current_raw_history)
                results.append(histories[index])
            except ValueError:
                raw_track = raw_history["track"]
                Track.createSimplifiedRaw(simpleRawTrack=raw_track, onExistRaiseError=onExistRaiseError)
                results.append(cls.create(**current_raw_history))
        return results
