from dataclasses import dataclass


@dataclass
class Fee:
    member_id: str
    amount: float
    donation: float

    def total(self) -> float:
        return self.amount + self.donation