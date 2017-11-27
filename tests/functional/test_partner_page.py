import re
# from .. import factories as f


def get_captcha_value(html_body):
    captcha_text = re.split(r'What is', html_body)[1]
    main_text = re.split(r'\?', captcha_text)
    a = main_text[0].strip().split(' ')
    if a[1] == '+':
        return int(a[0]) + int(a[2])
    if a[1] == '-':
        return int(a[0]) - int(a[2])
    if a[1] in ['*', '×']:
        return int(a[0]) * int(a[2])


def test_partner_page(base_url, browser, outbox):

    url = base_url + '/partner/'
    browser.visit(url)
    browser.fill('name', 'Full Name')
    browser.fill('email', 'test@test.org')
    browser.fill('comments', 'test@test.org')
    browser.select('partner_type', 'profit')
    browser.fill('contact_number', 999911)
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('This field is required.')

    browser.visit(url)
    browser.fill('org_name', 'Org Name')
    browser.fill('org_url', 'https://github.com/')
    browser.fill('name', 'Full Name')
    browser.fill('email', 'test@test.org')
    browser.fill('comments', 'test@test.org')
    browser.select('partner_type', 'profit')
    browser.fill('contact_number', 999911)
    captcha_value = get_captcha_value(browser.html)
    browser.fill('captcha_0', captcha_value)
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('Contact Number should be of 10 digits')

    browser.visit(url)
    browser.fill('org_name', 'Org Name')
    browser.fill('org_url', 'https://github.com/')
    browser.fill('name', 'Full Name')
    browser.fill('email', 'test@test.org')
    browser.fill('comments', 'test@test.org')
    browser.select('partner_type', 'profit')
    browser.fill('contact_number', 9999111111)
    browser.fill('description', 'description')
    browser.fill('python_use', 'python_use')
    captcha_value = get_captcha_value(browser.html)
    browser.fill('captcha_0', captcha_value)
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('Thank')
