import allure
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxDriver
from selenium.webdriver.remote.webelement import WebElement

from ..base.base_page import BasePage
from .search_page_locators import SearchPageLocators


class SearchPage(BasePage):
    title = 'Your Store'

    def __init__(self, driver: ChromeDriver | FirefoxDriver = None):
        super().__init__(driver=driver)
        self.driver = driver
        self.url = 'http://192.168.1.5:8081/index.php?route=product/search'

    @allure.step
    def find_results(self) -> list[WebElement] | str:
        try:
            p = self.driver.find_element(*SearchPageLocators.non_result_message)
            return p.text
        except NoSuchElementException:
            return self.find_elements(SearchPageLocators.searched_items_links)
