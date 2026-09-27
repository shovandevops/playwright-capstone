from typing import Any, Dict, List

from playwright.sync_api import APIResponse

from api_clients.base_client import ApiClientError, BaseApiClient
from models.user_model import User
from utils.logger import log_data


class UsersClient(BaseApiClient):
    """Service object handling User endpoint requests."""

    endpoint = "users"

    def get_users(self) -> List[User]:
        """Returns all users as User models. Raises ApiClientError on failure."""
        return User.from_json_list(self.get_users_raw())

    def get_users_raw(self) -> List[Dict[str, Any]]:
        """Returns the raw users JSON list for deep comparison testing."""
        response = self._send("get", self.endpoint)
        self.ensure_ok(response, "fetch users")
        data = self.parse_json(response)
        if not isinstance(data, list):
            raise ApiClientError(
                f"Expected a JSON list from {response.url}, got {type(data).__name__}",
                status=response.status,
                url=response.url,
            )
        return data

    def create_user(self, payload: Dict[str, Any]) -> APIResponse:
        """Req #14: Create a new user."""
        log_data(self.logger, {"payload": payload})
        return self._send("post", self.endpoint, data=payload)

    def update_user(self, user_id: int, payload: Dict[str, Any]) -> APIResponse:
        """Req #15: Update an existing user."""
        log_data(self.logger, {"user_id": user_id, "payload": payload})
        return self._send("put", f"{self.endpoint}/{user_id}", data=payload)

    def delete_user(self, user_id: int) -> APIResponse:
        """Req #16: Delete an existing user."""
        log_data(self.logger, {"user_id": user_id})
        return self._send("delete", f"{self.endpoint}/{user_id}")
