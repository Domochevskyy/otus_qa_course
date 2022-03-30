from page_object.models.models import AuthData


class TestAdminPage:
    def test_add_product(self, admin_page):
        admin_page.driver.get(admin_page.auth_admin_page.url)
        admin_page.auth_admin_page.login(AuthData.LOGIN, AuthData.PASSWORD)
        admin_page.product_page.add_product(name='a', tag_title='a', model='a')
        assert admin_page.product_page.is_product_found('a')

    def test_delete_product(self, admin_page):
        admin_page.product_page.delete_product('a')
        assert not admin_page.product_page.is_product_found('a')
