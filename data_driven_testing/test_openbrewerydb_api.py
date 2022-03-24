import pytest
from jsonschema import validate


class TestBreweryDBApi:
    def test_single_brewery(self, base_url, request_method, status_code):
        schema = {
            'type': 'object',
            'properties': {
                'id': {'type': 'string'},
                'name': {'type': 'string'},
                'brewery_type': {'type': 'string'},
                'street': {'type': 'string'},
                'address_2': {'type': ['string', 'null']},
                'address_3': {'type': ['string', 'null']},
                'city': {'type': 'string'},
                'state': {'type': 'string'},
                'county_province': {'type': ['string', 'null']},
                'postal_code': {'type': 'string'},
                'country': {'type': 'string'},
                'longitude': {'type': 'string'},
                'latitude': {'type': 'string'},
                'phone': {'type': 'string'},
                'website_url': {'type': 'string'},
                'updated_at': {'type': 'string'},
                'created_at': {'type': 'string'},
            },
        }
        uri = base_url + '/breweries/madtree-brewing-cincinnati'
        response = request_method(uri)
        validate(instance=response.json(), schema=schema)
        assert response.status_code == status_code

    def test_brewery_list(self, base_url, request_method, status_code):
        schema = {
            'type': 'array',
            'items': {
                'properties': {
                    'id': {'type': 'string'},
                    'name': {'type': 'string'},
                    'brewery_type': {'type': 'string'},
                    'street': {'type': ['null', 'string']},
                    'address_2': {'type': ['string', 'null']},
                    'address_3': {'type': ['string', 'null']},
                    'city': {'type': 'string'},
                    'state': {'type': ['null', 'string']},
                    'county_province': {'type': ['string', 'null']},
                    'postal_code': {'type': 'string'},
                    'country': {'type': 'string'},
                    'longitude': {'type': ['null', 'string']},
                    'latitude': {'type': ['null', 'string']},
                    'phone': {'type': ['null', 'string']},
                    'website_url': {'type': ['string', 'null']},
                    'updated_at': {'type': 'string'},
                    'created_at': {'type': 'string'},
                },
            }
        }
        uri = base_url + '/breweries'
        response = request_method(uri)
        validate(instance=response.json(), schema=schema)
        assert response.status_code == status_code

    @pytest.mark.parametrize('number', [1, 2, 25, 50, pytest.param(100, marks=pytest.mark.xfail)])
    def test_brewery_per_page(self, base_url, request_method, status_code, number):
        schema = {
            'type': 'array',
            'items': {
                'properties': {
                    'id': {'type': 'string'},
                    'name': {'type': 'string'},
                    'brewery_type': {'type': 'string'},
                    'street': {'type': ['null', 'string']},
                    'address_2': {'type': ['string', 'null']},
                    'address_3': {'type': ['string', 'null']},
                    'city': {'type': 'string'},
                    'state': {'type': ['null', 'string']},
                    'county_province': {'type': ['string', 'null']},
                    'postal_code': {'type': 'string'},
                    'country': {'type': 'string'},
                    'longitude': {'type': ['null', 'string']},
                    'latitude': {'type': ['null', 'string']},
                    'phone': {'type': ['null', 'string']},
                    'website_url': {'type': ['string', 'null']},
                    'updated_at': {'type': 'string'},
                    'created_at': {'type': 'string'},
                },
            }
        }
        uri = base_url + f'/breweries?per_page={number}'
        response = request_method(uri)
        parsed_response = response.json()
        validate(instance=parsed_response, schema=schema)
        assert len(parsed_response) == number
        assert response.status_code == status_code

    @pytest.mark.parametrize('br_type', ['micro', 'nano', 'regional', 'brewpub', 'large', 'planning'])
    def test_test_brewery_per_page_by_type(self, base_url, request_method, status_code, br_type):
        schema = {
            'type': 'array',
            'items': {
                'properties': {
                    'id': {'type': 'string'},
                    'name': {'type': 'string'},
                    'brewery_type': {'const': f'{br_type}'},
                    'street': {'type': ['null', 'string']},
                    'address_2': {'type': ['string', 'null']},
                    'address_3': {'type': ['string', 'null']},
                    'city': {'type': 'string'},
                    'state': {'type': ['null', 'string']},
                    'county_province': {'type': ['string', 'null']},
                    'postal_code': {'type': 'string'},
                    'country': {'type': 'string'},
                    'longitude': {'type': ['null', 'string']},
                    'latitude': {'type': ['null', 'string']},
                    'phone': {'type': ['null', 'string']},
                    'website_url': {'type': ['string', 'null']},
                    'updated_at': {'type': 'string'},
                    'created_at': {'type': 'string'},
                },
            }
        }
        uri = base_url + f'/breweries?by_type={br_type}'
        response = request_method(uri)
        validate(instance=response.json(), schema=schema)
        assert response.status_code == status_code

    @pytest.mark.parametrize('city', ['Knox', 'Bend', 'Boise', 'Killeshin', 'Mesa'])
    def test_brewery_by_city(self, base_url, request_method, status_code, city):
        schema = {
            'type': 'array',
            'items': {
                'properties': {
                    'id': {'type': 'string'},
                    'name': {'type': 'string'},
                    'brewery_type': {'type': 'string'},
                    'street': {'type': ['null', 'string']},
                    'address_2': {'type': ['string', 'null']},
                    'address_3': {'type': ['string', 'null']},
                    'city': {'type': 'string'},
                    'state': {'type': ['null', 'string']},
                    'county_province': {'type': ['string', 'null']},
                    'postal_code': {'type': 'string'},
                    'country': {'type': 'string'},
                    'longitude': {'type': ['null', 'string']},
                    'latitude': {'type': ['null', 'string']},
                    'phone': {'type': ['null', 'string']},
                    'website_url': {'type': ['string', 'null']},
                    'updated_at': {'type': 'string'},
                    'created_at': {'type': 'string'},
                },
            }
        }
        uri = base_url + f'/breweries?by_city={city}'
        response = request_method(uri)
        parsed_response = response.json()
        validate(instance=parsed_response, schema=schema)
        for key in parsed_response:
            assert city in key['city']
        assert response.status_code == status_code
