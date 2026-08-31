from dataclasses import dataclass

@dataclass
class User:
    id: str
    name: str
    email: str
    preferred_name: str | None = None

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Name cannot be empty")

        if "@" not in self.email:
            raise ValueError("Invalid email")