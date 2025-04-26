from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.core.entities.user import User

class UserRepository(ABC):

    @abstractmethod
    def add(self, user: User) -> None:
        pass

    @abstractmethod
    def get(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    def list(self) -> List[User]:
        pass