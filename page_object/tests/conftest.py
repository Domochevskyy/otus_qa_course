import pytest
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxDriver

from page_object.models.models import User
from page_object.pages import MainPage, SearchPage
from page_object.pages import AdminPage
from page_object.pages import RegistrationPage


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


@pytest.fixture()
def main_page(browser):
    return MainPage(browser)


@pytest.fixture()
def search_page(browser):
    return SearchPage(browser)


@pytest.fixture()
def admin_page(browser):
    return AdminPage(browser)


@pytest.fixture()
def registration_page(browser):
    return RegistrationPage(browser)


@pytest.fixture()
def delete_user(admin_page):
    yield
    admin_page.driver.refresh()
    admin_page.customers_page.delete(User.first_name, User.last_name)
