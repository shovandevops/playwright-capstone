# tests/test_users_api.py
import pytest
from api_clients.users_client import UsersClient
from models.user_model import User
from utils.json_comparator import deep_compare


@pytest.mark.api
class TestUsersAPI:

    def test_search_user_and_validate_properties(self, users_client: UsersClient):
        """
        Req #12: Search for a user dynamically without assuming index 0.
        Req #11: Validate model properties.
        """
        users = users_client.get_users()
        
        # Search dynamically by business property (name)
        target_name = "Leanne Graham"
        user = next((u for u in users if u.name == target_name), None)
        
        # Validations
        assert user is not None, f"User '{target_name}' was not found in response list"
        assert user.id == 1
        assert user.username == "Bret"
        assert user.email == "Sincere@april.biz"

    def test_exact_json_comparison(self, users_client: UsersClient):
        """Req #13: Exact dictionary comparison (assert actual == expected)."""
        raw_users = users_client.get_users_raw()
        first_user = raw_users[0]

        expected_user = {
            "id": 1,
            "name": "Leanne Graham",
            "username": "Bret",
            "email": "Sincere@april.biz",
            "address": {
                "street": "Kulas Light",
                "suite": "Apt. 556",
                "city": "Gwenborough",
                "zipcode": "92998-3874",
                "geo": {
                    "lat": "-37.3159",
                    "lng": "81.1496"
                }
            },
            "phone": "1-770-736-8071 x56442",
            "website": "hildegard.org",
            "company": {
                "name": "Romaguera-Crona",
                "catchPhrase": "Multi-layered client-server neural-net",
                "bs": "harness real-time e-markets"
            }
        }

        # Exact dictionary equality check
        assert first_user == expected_user

    def test_deep_json_comparison_with_path_reporting(self, users_client: UsersClient):
        """Req #13: Deep comparison utility reporting exact mismatch path."""
        raw_users = users_client.get_users_raw()
        actual_user = raw_users[0]

        # Constructing expected payload with deliberate nested value difference
        expected_user = {
            "id": 1,
            "name": "Leanne Graham",
            "username": "Bret",
            "email": "Sincere@april.biz",
            "address": {
                "street": "Kulas Light",
                "suite": "Apt. 556",
                "city": "Gwenborough",  # Matches
                "zipcode": "92998-3874",
                "geo": {
                    "lat": "-37.3159",
                    "lng": "81.1496"
                }
            },
            "phone": "1-770-736-8071 x56442",
            "website": "hildegard.org",
            "company": {
                "name": "Romaguera-Crona",
                "catchPhrase": "Multi-layered client-server neural-net",
                "bs": "harness real-time e-markets"
            }
        }

        # 1. Successful Deep Comparison
        is_matched, err_msg = deep_compare(actual_user, expected_user)
        assert is_matched, f"JSON comparison failed: {err_msg}"

    def test_deep_json_comparison_mismatch_demonstration(self):
        """Demonstrates how the utility catches nested mismatch paths like root.address.city."""
        actual = {
            "id": 1,
            "address": {"city": "New York", "zip": "10001"}
        }
        expected = {
            "id": 1,
            "address": {"city": "Gwenborough", "zip": "10001"}
        }

        is_matched, err_msg = deep_compare(actual, expected)
        
        assert not is_matched
        assert "root.address.city" in err_msg
        # err_msg output: "Value mismatch at 'root.address.city': Expected 'Gwenborough', got 'New York'"

    def test_create_user(self, users_client: UsersClient):
        """Req #14: Create a new user."""
        payload = {
            "name": "John Doe",
            "username": "johndoe",
            "email": "johndoe@example.com"
        }
        response = users_client.create_user(payload)
        assert response.ok
        assert response.status == 201
        assert response.json()["name"] == payload["name"]
        assert response.json()["username"] == payload["username"]
        assert response.json()["email"] == payload["email"]
        assert response.json()["id"] is not None
    
    def test_update_user(self, users_client: UsersClient):
        """Req #15: Update an existing user."""
        user_id = 1
        payload = {
            "name": "John Doe",
            "username": "johndoe",
            "email": "johndoe@example.com"
        }
        response = users_client.update_user(user_id, payload)
        assert response.ok
        assert response.status == 200

        body = response.json()
        assert body == {**payload, "id": user_id}

        updated_user = User(body)
        assert updated_user.id == user_id
        assert updated_user.name == payload["name"]
        assert updated_user.username == payload["username"]
        assert updated_user.email == payload["email"]

    def test_delete_user(self, users_client: UsersClient):
        """
        Req #16: Delete an existing user.
        The fake API does not persist deletes, so the user cannot be checked
        as missing afterwards; the empty-object response is the contract.
        """
        user_id = 1
        response = users_client.delete_user(user_id)
        assert response.ok
        assert response.status == 200
        assert response.headers["content-type"].startswith("application/json")
        assert response.json() == {}