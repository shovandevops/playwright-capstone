from api_clients.posts_client import PostsClient
import pytest

@pytest.mark.api
class TestPostsAPI:
    def test_get_all_posts(self, posts_client: PostsClient):
        response = posts_client.get_all_posts()
        assert response.ok
        assert response.status == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_post_by_id(self, posts_client: PostsClient):
        response = posts_client.get_post_by_id(1)
        assert response.ok
        post = response.json()
        assert post['id'] == 1
        assert 'title' in post
    
    def test_create_new_post(self, posts_client: PostsClient):
        payload = {"title": "Automated Test", "author": "QA Engineer"}
        response = posts_client.create_post(payload)
        
        assert response.status == 201
        
        body = response.json()
        assert body["title"] == payload["title"]
        assert body["author"] == payload["author"]
        assert "id" in body
    
    def test_delete_post(self, posts_client: PostsClient):
        response = posts_client.delete_post(1)
        assert response.status == 200
    
    def test_update_post(self, posts_client: PostsClient):
        payload = {"title": "Updated Test", "author": "QA Engineer"}
        response = posts_client.update_post(1, payload)
        assert response.status == 200
        
        body = response.json()
        assert body["title"] == payload["title"]
        assert body["author"] == payload["author"]
        assert "id" in body