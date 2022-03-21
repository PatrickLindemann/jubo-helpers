from dataclasses import dataclass
from datetime import date

@dataclass
class Member:
    id: int
    salutation: str
    first_name: str
    last_name: str
    street: str
    house_number: str
    zip_code: int
    city: str
    email: str
    phone_fixed: str
    phone_mobile: str
    birth_date: date
    age: int
    status: str
    membership: str
    role: str
    position: str
    join_date: date
    exit_date: date
    occupation: str
    comment: str