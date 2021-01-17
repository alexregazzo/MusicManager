from __future__ import annotations
from .base import Base
from .exceptions import *


class Profile(Base):
    def __init__(self, *,
                 pro_name: str,
                 pro_gain_integral: float,
                 pro_gain_derivative: float,
                 pro_gain_proporcional: float):
        self.pro_name = pro_name
        self.pro_gain_integral = pro_gain_integral
        self.pro_gain_derivative = pro_gain_derivative
        self.pro_gain_proporcional = pro_gain_proporcional

    @classmethod
    def table_pk(cls) -> str:
        return "pro_name"

    @classmethod
    def create(cls, *,
               pro_name: str,
               pro_gain_integral: float,
               pro_gain_derivative: float,
               pro_gain_proporcional: float,
               onExistRaiseError: bool = True
               ) -> Profile:

        try:
            cls._insert(pro_name=pro_name,
                        pro_gain_integral=pro_gain_integral,
                        pro_gain_derivative=pro_gain_derivative,
                        pro_gain_proporcional=pro_gain_proporcional)
        except ObjectAlreadyExistError:
            if onExistRaiseError:
                raise
        return cls.get(pro_name=pro_name)
