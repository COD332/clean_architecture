from uuid import UUID, uuid4

class User:
    def __init__(
        self,
        name: str,
        id: UUID = None,
    ):
        self.id: UUID = id or uuid4()
        self.name = name
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
        }
    
    def from_dict(data):
        return User(
            name=data["name"],
            id=UUID(data["id"]),
        )