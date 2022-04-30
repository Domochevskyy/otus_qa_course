import allure
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxDriver
from selenium.webdriver.remote.webelement import WebElement

from ...models import CurrencyChoice, CurrencyType
from ..base.base_page import BasePage
from .main_page_locators import MainPageLocators


class MainPage(BasePage):
    title = 'Your Store'

    def __init__(self, driver: ChromeDriver | FirefoxDriver = None):
        super().__init__(driver=driver)
        self.driver = driver
        self.url = 'http://192.168.1.5:8081/'

    @property
    def currency(self) -> CurrencyType:
        currency_display = self.find_element(MainPageLocators.currency_type).text
        for currency in CurrencyType:
            if currency.value == currency_display:
                return currency.value

    @currency.setter
    def currency(self, currency: CurrencyChoice) -> None:
        button = self.find_element(MainPageLocators.currency_button)
        self.click(button)

        button = None
        match currency:
            case CurrencyChoice.EURO:
                button = self.find_element(MainPageLocators.euro)
            case CurrencyChoice.POUND:
                button = self.find_element(MainPageLocators.pound)
            case CurrencyChoice.DOLLAR:
                button = self.find_element(MainPageLocators.dollar)
            case _:
                raise TypeError('Wrong currency was being chosen')
        self.click(element=button)

    @allure.step
    def search_product(self, product: str) -> None:
        search_input = self.find_element(MainPageLocators.search_input)
        self.send_keys(input_element=search_input, keys=product)
        search_button = self.find_element(MainPageLocators.search_button)
        self.click(element=search_button)

    @property
    def nav_bar(self) -> list[WebElement]:
        nav_bar = self.find_elements(MainPageLocators.nav_bar)
        return nav_bar

    @staticmethod
    def text_from(elements: list[WebElement] | WebElement = None) -> list[str] | str:
        if not isinstance(elements, list):
            return elements.text
        return list(map(lambda element: element.text, elements))
