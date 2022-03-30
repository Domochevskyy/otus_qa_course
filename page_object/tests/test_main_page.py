import pytest

from page_object.models import CurrencyType, CurrencyChoice


class TestMainPage:
    currency_displays = list(map(lambda currency: currency.value, CurrencyType))
    currency_choices = list(map(lambda currency: currency, CurrencyChoice))
    searched_product = 'imac'
    nav_bar_links = [
        'Desktops', 'Laptops & Notebooks',
        'Components', 'Tablets',
        'Software', 'Phones & PDAs',
        'Cameras', 'MP3 Players'
    ]

    @pytest.mark.parametrize(argnames='currency_type, currency_choice',
                             argvalues=zip(currency_displays, currency_choices))
    def test_currency(self, currency_type, currency_choice, main_page):
        main_page.driver.get(main_page.url)

        main_page.currency = currency_choice
        assert main_page.currency == currency_type

    def test_title(self, main_page):
        assert main_page.title == main_page.driver.title

    def test_search(self, main_page, search_page):
        main_page.search_product(self.searched_product)
        products = search_page.find_results()
        assert len(products) == 1

    def test_nav_bar(self, main_page):
        main_page.driver.get(main_page.url)
        elements = main_page.nav_bar
        assert main_page.text_from(elements)
