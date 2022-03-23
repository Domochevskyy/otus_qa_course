import pytest
import requests


def pytest_addoption(parser):
    parser.addoption(
        '--url',
        help='Url to test',
        required=True,
    )

    parser.addoption(
        '--method',
        default='get',
        choices=['get', 'post', 'put', 'patch', 'delete'],
        help='Method to test',
    )

    parser.addoption(
        '--status_code',
        default='200',
        help='Response status'
    )


@pytest.fixture
def base_url(request) -> str:
    return request.config.getoption('--url')


@pytest.fixture
def request_method(request) -> requests.models.Response():
    return getattr(requests, request.config.getoption('--method'))


@pytest.fixture
def status_code(request) -> int:
    return int(request.config.getoption('--status_code'))
