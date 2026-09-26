# clients/users_client.py
from typing import List
from playwright.sync_api import APIRequestContext, APIResponse
from models.user_model import User
from typing import Dict, Any
from utils.logger import get_logger, log_step, log_data


class UsersClient:
    """Service object handling User endpoint requests."""

    def __init__(self, request_context: APIRequestContext):
        self.request = request_context
        self.endpoint = "users"
        self.logger = get_logger("UsersClient")
        log_step(self.logger, "UsersClient initialized")

    def get_users(self) -> List[User]:
        log_step(self.logger, "Getting users")
        response = self.request.get(self.endpoint)
        log_step(self.logger, "Users retrieved")
        log_data(self.logger, {"response": response.json()})
        assert response.ok, f"Failed to fetch users: {response.status}"
        return User.from_json_list(response.json())

    def get_users_raw(self):
        """Returns raw JSON response for deep comparison testing."""
        log_step(self.logger, "Getting users raw")
        response = self.request.get(self.endpoint)
        return response.json()
    
    def create_user(self, payload: Dict[str, Any]) -> APIResponse:
        """Req #14: Create a new user."""
        log_step(self.logger, "Creating user")
        log_data(self.logger, {"payload": payload})
        response = self.request.post(self.endpoint, data=payload)
        log_step(self.logger, "User created")
        log_data(self.logger, {"response": response.json()})
        return response
    
    def update_user(self, user_id: int, payload: Dict[str, Any]) -> APIResponse:
        """Req #15: Update an existing user."""
        log_step(self.logger, "Updating user")
        log_data(self.logger, {"payload": payload})
        response = self.request.put(f"{self.endpoint}/{user_id}", data=payload)
        log_step(self.logger, "User updated")
        log_data(self.logger, {"response": response.json()})
        return response
    
    def delete_user(self, user_id: int) -> APIResponse:
        """Req #16: Delete an existing user."""
        log_step(self.logger, "Deleting user")
        log_data(self.logger, {"user_id": user_id})
        response = self.request.delete(f"{self.endpoint}/{user_id}")
        log_step(self.logger, "User deleted")
        log_data(self.logger, {"response": response.json()})
        return response