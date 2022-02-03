import pytest


@pytest.fixture()
def list_all_breeds_url(config):
    return config['list_all_breeds']


@pytest.fixture()
def random_image_url(config):
    return config['random_image']


@pytest.fixture()
def list_all_sub_breeds_url(config):
    return config['list_all_sub_breeds']
