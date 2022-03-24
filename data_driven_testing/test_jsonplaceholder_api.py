import pytest
import requests
from jsonschema import validate


class InvalidStatusCode(Exception):
    def __init__(self, text):
        self.txt = text


class TestJsonPlaceHolder:
    end_points = [("posts", 100), ("comments", 500), ("albums", 100), ("photos", 5000), ("todos", 200), ("users", 10)]

    @pytest.fixture()
    def post_info(self, base_url):
        request_params = {
            'uri': f'{base_url}posts',
            'body': {"title": "foo", "body": "bar", "userId": 1},
            'headers': {"Content-type": "application/json; charset=UTF-8"}
        }
        return request_params

    @pytest.mark.parametrize('end_point', ['posts', 'comments', 'albums', 'photos', 'todos', 'users'])
    def tests_resources_status_code(self, base_url, request_method, status_code, end_point):
        uri = base_url + end_point
        response = request_method(uri)
        assert response.status_code == status_code

    def test_create_post(self, base_url, post_info):
        schema = {
            'type': 'object',
            'properties': {
                'title': {'type': 'string'},
                'body': {'type': 'string'},
                'userId': {'type': 'number'},
                'id': {'type': 'number'},
            },
            "required": ['title', 'body', 'userId', 'id']
        }
        response = requests.post(url=post_info['uri'], headers=post_info['headers'], json=post_info['body'])
        validate(instance=response.json(), schema=schema)
        assert response.status_code == 201

    def test_patch_post(self, base_url, post_info):
        schema = {
            'type': 'object',
            'properties': {
                'title': {'type': 'string'},
                'body': {'type': 'string'},
                'userId': {'type': 'number'},
                'id': {'type': 'number'},
            },
            "required": ['title', 'body', 'userId', 'id']
        }
        response = requests.patch(base_url + 'posts/1', json=post_info['body'])
        validate(instance=response.json(), schema=schema)
        assert response.status_code == 200

    def test_delete_post(self, base_url):
        response = requests.delete(base_url + 'posts/1')
        assert response.status_code == 200

    @pytest.mark.parametrize("end_point, expected_number", end_points)
    def test_number_of_returned_items(self, base_url, end_point, expected_number):
        response = requests.get(base_url + f'{end_point}')
        assert len(response.json()) == expected_number
        assert response.status_code == 200
