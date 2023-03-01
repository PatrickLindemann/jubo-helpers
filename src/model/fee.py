from dataclasses import dataclass


@dataclass
class Fee:
    member_id: str
    amount: float
    donation: float

    def __post_init__(self):
        self.amount = self.amount if self.amount else 0.0
        self.donation = self.donation if self.donation else 0.0

    def total(self) -> float:
        return self.amount + self.donation