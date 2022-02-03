import pytest
import yaml


def pytest_addoption(parser):
    parser.addoption(
        "--config", action="store", help="config file path", required=True
    )


@pytest.fixture(scope="session")
def config(request):
    with open(request.config.getoption("--config"), 'r') as stream:
        try:
            parsed_yaml = yaml.safe_load(stream)
        except yaml.YAMLError:
            raise
    return parsed_yaml
