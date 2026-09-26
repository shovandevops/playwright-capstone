from playwright.sync_api import APIRequestContext, APIResponse
from typing import Dict, Any
from utils.logger import get_logger, log_step, log_data

class PostsClient:
    def __init__(self, request_context: APIRequestContext):
        self.request = request_context
        self.endpoint = "/posts"
        self.logger = get_logger("PostsClient")
        log_step(self.logger, "PostsClient initialized")

    def get_all_posts(self) -> APIResponse:
        log_step(self.logger, "Getting all posts")
        response = self.request.get(self.endpoint)
        log_step(self.logger, "All posts retrieved")
        log_data(self.logger, {"response": response.json()})
        return response

    def get_post_by_id(self, post_id: int) -> APIResponse:
        log_step(self.logger, "Getting post by id")
        response = self.request.get(f"{self.endpoint}/{post_id}")
        log_step(self.logger, "Post retrieved")
        log_data(self.logger, {"response": response.json()})
        return response

    def create_post(self, payload: Dict[str, Any]) -> APIResponse:
        log_step(self.logger, "Creating post")
        log_data(self.logger, {"payload": payload})
        response = self.request.post(self.endpoint, data=payload)
        log_step(self.logger, "Post created")
        log_data(self.logger, {"response": response.json()})
        return response
    
    def update_post(self, post_id: int, payload: Dict[str, Any]) -> APIResponse:
        log_step(self.logger, "Updating post")
        log_data(self.logger, {"payload": payload})
        response = self.request.put(f"{self.endpoint}/{post_id}", data=payload)
        log_step(self.logger, "Post updated")
        log_data(self.logger, {"response": response.json()})
        return response
    
    def delete_post(self, post_id: int) -> APIResponse:
        log_step(self.logger, "Deleting post")
        response = self.request.delete(f"{self.endpoint}/{post_id}")
        log_step(self.logger, "Post deleted")
        log_data(self.logger, {"response": response.json()})
        return response