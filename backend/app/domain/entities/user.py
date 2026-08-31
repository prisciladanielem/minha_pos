import re
from dataclasses import dataclass
from dataclasses import dataclass, field
from uuid import UUID, uuid4

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

@dataclass
class User:
    name: str
    email: str
    preferred_name: str | None = None
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        self.email = self.email.lower()

        if not self.id:
            raise ValueError("Id cannot be empty")
        
        if not self.name.strip():
            raise ValueError("Name cannot be empty")

        if self.preferred_name is not None and not self.preferred_name.strip():
            raise ValueError("Preferred name cannot be empty")

        if not _EMAIL_RE.match(self.email):
            raise ValueError("Invalid email")
