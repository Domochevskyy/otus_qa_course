import allure
from models import AuthData, User


class TestRegistrationPage:

    @allure.title('Registration')
    def test_registration(self, registration_page, admin_page, delete_user):
        with allure.step('Get registration page'):
            registration_page.driver.get(registration_page.url)
        registration_page.register_account(data=User)
        with allure.step('Get login page'):
            registration_page.driver.get(admin_page.auth_admin_page.url)
        admin_page.auth_admin_page.login(AuthData.LOGIN, AuthData.PASSWORD)
        assert admin_page.customers_page.is_customer_found(User.first_name, User.last_name)
