import pytest
import requests
from jsonschema import validate


class TestAllListBreeds:
    json_schema = {
        'type': 'object',
        'properties': {
            'message': {'type': 'object'},
            'status': {'type': 'string'},
        },
        'required': ['message', 'status']
    }

    def test_valid_status_code(self, list_all_breeds_url):
        response = requests.get(url=list_all_breeds_url)
        assert response.status_code == 200

    def test_json_schema(self, list_all_breeds_url):
        response = requests.get(url=list_all_breeds_url)
        response_json = response.json()
        validate(response_json, TestAllListBreeds.json_schema)

    def test_invalid_status_code(self, list_all_breeds_url):
        invalid_endpoint = 'kekw'
        response = requests.get(url=list_all_breeds_url + invalid_endpoint)
        assert response.status_code == 404


class TestRandomImage:
    json_schema = {
        'type': 'object',
        'properties': {
            'message': {'type': 'string'},
            'status': {'type': 'string'},
        },
        'required': ['message', 'status']
    }

    def test_json_schema(self, random_image_url):
        response = requests.get(url=random_image_url)
        response_json = response.json()
        validate(response_json, TestRandomImage.json_schema)

    @pytest.mark.parametrize('value', [i for i in range(1, 6)])
    def test_multiple_random_images(self, value, random_image_url):
        url = random_image_url + '/' + str(value)
        response = requests.get(url=url)
        assert response.status_code == 200
        assert len(response.json()['message']) == value

    def test_multiple_random_images_max(self, random_image_url):
        url = random_image_url + '/' + str(100)
        response = requests.get(url=url)
        assert response.status_code == 200
        assert len(response.json()['message']) == 50


class TestListAllSubBreeds:
    json_schema = {
        'type': 'object',
        'properties': {
            'message': {
                'type': 'array',
                'prefixItems': [
                    {'const': 'afghan'},
                    {'const': 'basset'},
                    {'const': 'blood'},
                    {'const': 'english'},
                    {'const': 'ibizan'},
                    {'const': 'plott'},
                    {'const': 'walker'},
                ]

            },
            'status': {'type': 'string'},
        },
        'required': ['message', 'status']
    }

    sub_breeds = ['afghan',
                  'basset',
                  'blood',
                  'english',
                  'ibizan',
                  'plott',
                  'walker',
                  ]

    def test_all_list_schema(self, list_all_sub_breeds_url):
        url = list_all_sub_breeds_url
        response = requests.get(url=url)
        validate(response.json(), TestListAllSubBreeds.json_schema)

    @pytest.mark.parametrize('value', sub_breeds)
    def test_all_sub_breed_images(self, value):
        url = f'https://dog.ceo/api/breed/hound/{value}/images'
        response = requests.get(url=url)
        assert response.status_code == 200
