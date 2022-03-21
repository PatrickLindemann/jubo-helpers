from dataclasses import dataclass
from datetime import date

@dataclass
class Bill:
    member_id: int
    first_name: str
    last_name: str
    street: str
    house_number: str
    zip_code: int
    city: str
    fee: float
    donation: float
    total: float
    last_payment_date: date
    creditor_id: str
    reference: str
    issue_date: date
    credit_institute: str
    iban: str
    bic: str

    def __post_init__(self):
        self.fee = self.fee if self.fee else 0.0
        self.donation = self.donation if self.donation else 0.0
        self.total = self.total if self.total else 0.0

    def anonymized_iban(self):
        return self.iban[0:3] + "XXXXXXXXXXXXXXX" + self.iban[-3:]
    
    def anonymized_bic(self):
        return self.bic[0:6] + "XXXXX"