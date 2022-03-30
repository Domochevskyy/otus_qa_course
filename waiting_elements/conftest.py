import pytest
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxDriver


def pytest_addoption(parser):
    parser.addoption('--browser', help='Web browser', required=True)
    parser.addoption('--url', help='Base opencart url', required=True)
    parser.addoption('--driver_path', required=True)


@pytest.fixture(scope='session')
def browser(request) -> ChromeDriver | FirefoxDriver:
    _browser = request.config.getoption('--browser').lower()
    driver_path = request.config.getoption('--driver_path')
    match _browser:
        case 'chrome':
            chrome_service = ChromeService(driver_path)
            _browser = ChromeDriver(service=chrome_service)
        case 'firefox':
            firefox_service = FirefoxService(driver_path)
            _browser = FirefoxDriver(service=firefox_service)
        case _:
            raise WebDriverException(msg='Invalid browser name.\nMake sure that name is chrome or firefox.')
    _browser.maximize_window()
    yield _browser
    _browser.close()
    _browser.quit()


@pytest.fixture(scope='session')
def base_url(request) -> str:
    _base_url = request.config.getoption('--url')
    return _base_url
