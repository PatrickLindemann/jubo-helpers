from dataclasses import dataclass
from datetime import date


@dataclass
class Mandate:
    id: str
    member_id: str
    first_name: str
    last_name: str
    street: str
    house_number: str
    zip_code: int
    city: str
    creditor_id: str
    issue_date: date
    iban: str
    bic: str
    credit_institute: str

    @property
    def reference(self) -> str:
        return self.id
    
    @reference.setter
    def reference(self, reference: str):
        self.reference = reference
        self.id = reference

    def formatted_iban(self) -> str:
        return self.iban[0:4] + ' ' + self.iban[4:8] + ' ' + self.iban[8:12]\
            + ' ' + self.iban[12:16] + ' ' + self.iban[16:20] + ' ' + self.iban[20:22]

    def anonymized_iban(self) -> str:
        return self.iban[0:3] + 'XXXXXXXXXXXXXXX' + self.iban[-3:]
    
    def anonymized_bic(self) -> str:
        return self.bic[0:6] + 'XXXXX'