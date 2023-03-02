from dataclasses import dataclass
from datetime import date
from typing import List

from src.model.mandate import Mandate
from src.model.member import Member


@dataclass
class Position:
    description: str
    amount: float

@dataclass
class Bill:
    member: Member
    mandate: Mandate
    positions: List[Position]
    creation_date: date
    value_date: date

    def total(self) -> float:
        return sum(position.amount for position in self.positions)