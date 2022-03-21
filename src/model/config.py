from dataclasses import dataclass
from typing import List

@dataclass
class User:
    email: str
    password: str

@dataclass
class Server:
    host: str
    port: int

@dataclass
class Config:
    user: User
    servers: List[Server]