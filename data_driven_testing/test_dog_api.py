from jsonschema import validate

import pytest


class TestDogApi:

    def test_random_image(self, base_url, request_method, status_code):
        schema = {
            'type': 'object',
            'properties': {
                'message': {
                    'type': 'string'
                },
                'status': {
                    'type': 'string'
                },
            },
            "required": ['message', 'status']
        }
        uri = base_url + '/breeds/image/random'
        response = request_method(uri)
        validate(instance=response.json(), schema=schema)
        assert response.status_code == status_code, 'Invalid status code.'

    def test_list_all_breeds(self, base_url, request_method, status_code):
        schema = {
            'properties': {
                'message': {
                    'type': 'object',
                },
                'status': {
                    'const': 'success',
                },

            },
        }
        uri = base_url + '/breeds/list/all'
        response = request_method(uri)
        validate(instance=response, schema=schema)
        assert response.status_code == status_code, 'Invalid status code.'

    def test_list_all_sub_breeds(self, base_url, request_method, status_code):
        schema = {
            'properties': {
                'message': {
                    'type': 'array',
                    'items': {
                        'type': 'string'
                    },
                },
                'status': {
                    'type': 'string',
                },
            },
        }
        uri = base_url + '/breed/hound/list'
        response = request_method(uri)
        validate(instance=response, schema=schema)
        assert response.status_code == status_code, 'Invalid status code.'

    @pytest.mark.parametrize('number', [1, 2, 50, pytest.param(100, marks=pytest.mark.xfail)])
    def test_several_random_images(self, base_url, number, request_method, status_code):
        schema = {
            'type': 'object',
            'properties': {
                'message': {
                    'type': 'array',
                    'maxItems': 50,
                    'minItems': 1,
                    'items': {
                        'type': 'string'
                    },
                },
                'status': {
                    'type': 'string',
                },
            },
        }
        uri = base_url + '/breeds/image/random/' + f'{number}'
        response = request_method(uri)
        parsed_response = response.json()
        validate(instance=parsed_response, schema=schema)
        assert len(parsed_response['message']) == number, 'The number of messages is not equal to number in param.'
        assert response.status_code == status_code, 'Invalid status code.'

    @pytest.mark.parametrize('breed', ['affenpinscher', 'african', 'akita', 'beagle'])
    def test_breeds_list(self, breed, base_url, request_method, status_code):
        schema = {
            'type': 'object',
            'properties': {
                'message': {
                    'type': 'string'
                },
                'status': {
                    'type': 'string'
                },
            },
            "required": ['message', 'status']
        }
        uri = base_url + f'/breed/{breed}/images/random'
        response = request_method(uri)
        validate(instance=response.json(), schema=schema)
        assert response.status_code == status_code, 'Invalid status code.'
