import allure
from models import AuthData


class TestAdminPage:

    @allure.title('Add product')
    def test_add_product(self, admin_page):
        with allure.step('Get login page'):
            admin_page.driver.get(admin_page.auth_admin_page.url)
        with allure.step('Login to open card'):
            admin_page.auth_admin_page.login(AuthData.LOGIN, AuthData.PASSWORD)
        with allure.step('Add product to open card'):
            admin_page.product_page.add_product(name='a', tag_title='a', model='a')
        assert admin_page.product_page.is_product_found('a')

    @allure.title('Delete product')
    def test_delete_product(self, admin_page):
        with allure.step('Delete product from open card'):
            admin_page.product_page.delete_product('a')
        assert not admin_page.product_page.is_product_found('a')
