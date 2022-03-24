from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class TestOpenCart:
    timeout = 20

    def test_main_page(self, browser, base_url):
        nav_bar_links = [
            'Desktops', 'Laptops & Notebooks',
            'Components', 'Tablets',
            'Software', 'Phones & PDAs',
            'Cameras', 'MP3 Players'
        ]
        currency_list = ['€ Euro', '£ Pound Sterling', '$ US Dollar']
        nav_bar_links_locator = (By.XPATH, '//div[@class="collapse navbar-collapse navbar-ex1-collapse"]/ul/li')
        currency_button_locator = (By.XPATH, '//button[@class="btn btn-link dropdown-toggle"]')
        currency_list_locator = (By.XPATH, '//div[@class="btn-group open"]/ul/li')

        browser.get(base_url)
        nav_links = WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_all_elements_located(nav_bar_links_locator))
        text_nav_links = [link.text for link in nav_links]
        assert nav_bar_links == text_nav_links

        currency_button = WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_element_located(currency_button_locator))
        currency_button.click()
        currency_list_from_page = WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_all_elements_located(currency_list_locator))
        text_currency_list = [currency.text for currency in currency_list_from_page]
        assert currency_list == text_currency_list

        contact_us_link_locator = (By.XPATH, '//a[i[@class="fa fa-phone"]]')
        contact_us_link = WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_element_located(contact_us_link_locator))
        old_title = browser.title
        contact_us_link.click()
        new_title = browser.title
        assert old_title != new_title and new_title == 'Contact Us'

        search_field_locator = (By.XPATH, '//input[@name="search"]')
        search_field = WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_element_located(search_field_locator))
        message = 'bruh'
        search_field.send_keys(message)

        search_button_locator = (By.XPATH, '//button[@class="btn btn-default btn-lg"]')
        search_button = WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_element_located(search_button_locator))
        search_button.click()

        search_result_locator = (By.XPATH, '//div/h1')
        search_result_display = WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_element_located(search_result_locator))
        assert message in search_result_display.text

    def test_catalog_page(self, browser, base_url):
        browser.get(base_url + '/desktops')
        catalog_target_locator = (By.XPATH, '//div[@id="content"]/h2')
        catalog_target = WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_element_located(catalog_target_locator))
        assert catalog_target.text == 'Desktops'

        products_quantity_on_page_locator = (By.XPATH, '//div[@class="image"]')
        products_quantity_on_page = WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_all_elements_located(products_quantity_on_page_locator))
        assert len(products_quantity_on_page) == 12

        apple_cinema_30_product_locator = (By.XPATH, "//a[text()='Apple Cinema 30\"']")
        apple_cinema_30_product_link = WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_element_located(apple_cinema_30_product_locator))
        apple_cinema_30_product_link.click()
        apple_cinema_30_product_display_locator = (By.XPATH, "//h1[text()='Apple Cinema 30\"']")
        apple_cinema_30_product_display = WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_element_located(apple_cinema_30_product_display_locator))
        assert apple_cinema_30_product_display.text == 'Apple Cinema 30\"'

        browser.get(base_url + '/desktops')
        add_to_wish_list_locator = (By.XPATH, '/html/body/div[2]/div/div/div[4]/div[1]/div/div[2]/div[2]/button[2]/i')
        add_to_wish_list = WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_element_located(add_to_wish_list_locator))
        add_to_wish_list.click()

        close_button_locator = (By.XPATH, '/html/body/div[2]/div[1]/button')
        close_button = WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_element_located(close_button_locator))
        close_button.click()
        flag = True
        try:
            WebDriverWait(browser, self.timeout).until(ec.invisibility_of_element(close_button))
        except TimeoutException:
            flag = False
        assert flag

    def test_product_cart_page(self, browser, base_url):
        browser.get(base_url)
        shopping_cart_button_locator = (By.XPATH, '//a[@title="Shopping Cart"]')
        shopping_cart_button = WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_element_located(shopping_cart_button_locator))
        shopping_cart_button.click()
        assert browser.title == 'Shopping Cart'

        continue_button_locator = (By.XPATH, '//a[text()="Continue"]')
        continue_button = WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_element_located(continue_button_locator))
        continue_button.click()
        assert browser.current_url == 'http://192.168.1.5:8081/index.php?route=common/home'

        browser.get(base_url + '/index.php?route=checkout/cart')
        empty_message_shop_cart_locator = (By.XPATH, '//div[@id="content"]/p')
        empty_message_shop_cart = WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_element_located(empty_message_shop_cart_locator))
        assert empty_message_shop_cart.text == 'Your shopping cart is empty!'

    def test_admin_page(self, browser, base_url):
        browser.get(base_url + '/admin')

        username = 'user'
        password = 'bitnami'
        username_locator = (By.XPATH, '//input[@name="username"]')
        password_locator = (By.XPATH, '//input[@name="password"]')
        login_button_locator = (By.XPATH, '//button[@type="submit"]')

        username_field = WebDriverWait(browser, self.timeout).until(ec.visibility_of_element_located(username_locator))
        username_field.send_keys(username)
        password_field = WebDriverWait(browser, self.timeout).until(ec.visibility_of_element_located(password_locator))
        password_field.send_keys(password)
        login_button = WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_element_located(login_button_locator))
        login_button.click()
        assert browser.title == 'Dashboard'

        navigation_selector = (By.CSS_SELECTOR, 'div#navigation')
        navigation = WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_element_located(navigation_selector))
        assert 'navigation' in navigation.text.lower()

        WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_element_located((By.XPATH, '//a[text()=" Reports"]'))).click()

        WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_element_located((By.XPATH, '/html/body/div/nav/ul/li[9]/ul/li[2]/a'))).click()

        refresh_button_locator = (By.XPATH, '//a[@data-original-title="Refresh"]')
        refresh_button = WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_element_located(refresh_button_locator))

        refresh_button.click()
        assert browser.title == 'Online Report'

        online_report_locator = (By.XPATH, '//h1')
        online_report = browser.find_element(*online_report_locator)
        assert online_report.text == 'Online Report'

    def test_registration_page(self, browser, base_url):
        browser.get(base_url + '/index.php?route=account/register')
        assert browser.title == 'Register Account'

        WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div[2]/div/div/form/div/div/input[2]'))).send_keys(Keys.SPACE)

        alert = WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]')))
        assert alert

        inputs = WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_all_elements_located(
                (By.XPATH, '//input[@class="form-control"]')))
        assert len(inputs) == 6

        assert not WebDriverWait(browser, self.timeout).until(
            ec.visibility_of_element_located(
                (By.XPATH, '/html/body/div[2]/div/div/form/fieldset[3]/div/div/label[1]/input'))).is_selected()
