from typing import Any, Dict

from playwright.sync_api import APIResponse

from api_clients.base_client import BaseApiClient
from utils.logger import log_data


class PostsClient(BaseApiClient):
    """Service object handling Post endpoint requests."""

    endpoint = "posts"

    def get_all_posts(self) -> APIResponse:
        return self._send("get", self.endpoint)

    def get_post_by_id(self, post_id: int) -> APIResponse:
        log_data(self.logger, {"post_id": post_id})
        return self._send("get", f"{self.endpoint}/{post_id}")

    def create_post(self, payload: Dict[str, Any]) -> APIResponse:
        log_data(self.logger, {"payload": payload})
        return self._send("post", self.endpoint, data=payload)

    def update_post(self, post_id: int, payload: Dict[str, Any]) -> APIResponse:
        log_data(self.logger, {"post_id": post_id, "payload": payload})
        return self._send("put", f"{self.endpoint}/{post_id}", data=payload)

    def delete_post(self, post_id: int) -> APIResponse:
        log_data(self.logger, {"post_id": post_id})
        return self._send("delete", f"{self.endpoint}/{post_id}")
