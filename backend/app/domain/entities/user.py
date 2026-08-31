import re
from dataclasses import dataclass

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

@dataclass
class User:
    id: str
    name: str
    email: str
    preferred_name: str | None = None

    def __post_init__(self):
        if not self.id.strip():
            raise ValueError("Id cannot be empty")
        
        if not self.name.strip():
            raise ValueError("Name cannot be empty")

        if not _EMAIL_RE.match(self.email):
            raise ValueError("Invalid email")