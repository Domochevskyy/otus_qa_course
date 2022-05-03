import logging

import allure
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxDriver

from page_object.models.models import User
from page_object.pages import BasePage

from .registration_page_locators import RegistrationPageLocators


class RegistrationPage(BasePage):
    def __init__(self, driver: ChromeDriver | FirefoxDriver = None):
        super().__init__(driver=driver)
        self.url = 'http://192.168.1.5:8081/index.php?route=account/register'

    @allure.step
    def register_account(self, data: User):
        first_name = self.find_element(RegistrationPageLocators.first_name)
        self.send_keys(input_element=first_name, keys=User.first_name)
        last_name = self.find_element(RegistrationPageLocators.last_name)
        self.send_keys(input_element=last_name, keys=User.last_name)
        email = self.find_element(RegistrationPageLocators.email)
        self.send_keys(input_element=email, keys=User.email)
        phone = self.find_element(RegistrationPageLocators.telephone)
        self.send_keys(input_element=phone, keys=User.telephone)
        password = self.find_element(RegistrationPageLocators.password)
        self.send_keys(input_element=password, keys=User.password)
        confirm_password = self.find_element(RegistrationPageLocators.confirm_password)
        self.send_keys(input_element=confirm_password, keys=User.password)

        agree_input = self.find_element(RegistrationPageLocators.agree_policy)
        self.send_keys(input_element=agree_input, keys=Keys.SPACE)
        continue_button = self.find_element(RegistrationPageLocators.continue_button)
        self.click(element=continue_button)
        logging.info(f'Account {User} was successfully registered.')
