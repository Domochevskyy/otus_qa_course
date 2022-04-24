from page_object.models.models import User, AuthData


class TestRegistrationPage:

    def test_registration(self, registration_page, admin_page, delete_user):
        registration_page.driver.get(registration_page.url)
        registration_page.register_account(data=User)
        registration_page.driver.get(admin_page.auth_admin_page.url)
        admin_page.auth_admin_page.login(AuthData.LOGIN, AuthData.PASSWORD)
        assert admin_page.customers_page.is_customer_found(User.first_name, User.last_name)
