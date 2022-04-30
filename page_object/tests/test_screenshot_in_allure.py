import allure


def test_screenshot(main_page):
    wrong_url = 'https://google.com'
    main_page.driver.get(wrong_url)
    main_page.driver.get_screenshot_as_file('failed_test.png')
    allure.attach.file(
        source='failed_test.png',
        attachment_type=allure.attachment_type.PNG,
    )
    assert main_page.title == main_page.driver.title
