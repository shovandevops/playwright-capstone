# models/user_model.py
from typing import Dict, Any, List

class User:
    """Response model for User endpoints with properties and validations."""

    def __init__(self, data: Dict[str, Any]):
        # Data validation upon initialization
        if not isinstance(data, dict):
            raise TypeError(f"Expected dict for User data, got {type(data).__name__}")
        
        self._id = data.get("id")
        self._name = data.get("name")
        self._username = data.get("username")
        self._email = data.get("email")
        self._address = data.get("address", {})

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def username(self) -> str:
        return self._username

    @property
    def email(self) -> str:
        return self._email

    @property
    def city(self) -> str:
        """Convenience property for nested address property."""
        return self._address.get("city", "")

    @classmethod
    def from_json_list(cls, json_list: List[Dict[str, Any]]) -> List["User"]:
        """Factory method to convert a list of dicts to a list of User objects."""
        return [cls(item) for item in json_list]