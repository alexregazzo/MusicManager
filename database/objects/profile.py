from __future__ import annotations

import typing

from .base import Base
from .exceptions import *


class GenericProfileJson(typing.TypedDict):
    ph: float
    phs: float
    pc: float
    pm: float


class GenericProfileRow(typing.TypedDict):
    ph: float
    phs: float
    pc: float
    pm: float


class Profile(Base):
    def __init__(self, *,
                 pro_id: int,
                 pro_ph: float,
                 pro_phs: float,
                 pro_pc: float,
                 pro_pm: float
                 ):
        self.pro_id = pro_id
        self.pro_ph = pro_ph
        self.pro_phs = pro_phs
        self.pro_pc = pro_pc
        self.pro_pm = pro_pm

    @classmethod
    def create(cls, *,
               pro_ph: float,
               pro_phs: float,
               pro_pc: float,
               pro_pm: float
               ) -> Profile:
        ident = cls._insert(pro_ph=pro_ph,
                            pro_phs=pro_phs,
                            pro_pc=pro_pc,
                            pro_pm=pro_pm)
        return cls.get(pro_id=ident)

    @classmethod
    def getOrCreate(cls, *,
                    pro_ph: float,
                    pro_phs: float,
                    pro_pc: float,
                    pro_pm: float,
                    ) -> Profile:
        try:
            return cls.get(pro_ph=pro_ph,
                           pro_phs=pro_phs,
                           pro_pc=pro_pc,
                           pro_pm=pro_pm)
        except ObjectDoesNotExistError:
            return cls.create(pro_ph=pro_ph,
                              pro_phs=pro_phs,
                              pro_pc=pro_pc,
                              pro_pm=pro_pm)

    def toGenDict(self) -> GenericProfileJson:
        return {
            "ph": self.pro_ph,
            "phs": self.pro_phs,
            "pc": self.pro_pc,
            "pm": self.pro_pm
        }

    @staticmethod
    def fromGenDict(data: GenericProfileJson) -> GenericProfileRow:
        return {
            "pro_ph": data["ph"],
            "pro_phs": data["phs"],
            "pro_pc": data["pc"],
            "pro_pm": data["pm"]
        }
