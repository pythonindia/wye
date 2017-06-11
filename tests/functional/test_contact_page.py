import re
# from .. import factories as f


def get_captcha_value(html_body):
    captcha_text = re.split(r'What is', html_body)[1]
    main_text = re.split(r'\?', captcha_text)
    a = main_text[0].strip().split(' ')
    print(a)
    if a[1] == '+':
        return int(a[0]) + int(a[2])
    if a[1] == '-':
        return int(a[0]) - int(a[2])
    if a[1] in ['*', '×']:
        return int(a[0]) * int(a[2])


def test_contact_page(base_url, browser, outbox):

    url = base_url + '/contact/'
    browser.visit(url)
    browser.fill('name', 'Full Name')
    browser.fill('email', 'test@test.org')
    browser.fill('comments', 'test@test.org')
    browser.fill('contact_number', 999911)
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('This field is required.')

    browser.visit(url)
    browser.fill('name', 'Full Name')
    browser.fill('email', 'test@test.org')
    browser.fill('comments', 'test@test.org')
    browser.fill('contact_number', 999911)
    captcha_value = get_captcha_value(browser.html)
    browser.fill('captcha_0', captcha_value)
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('Contact Number should be of 10 digits')

    browser.visit(url)
    url = base_url + '/contact/'
    browser.fill('name', 'Full Name')
    browser.fill('email', 'test@test.org')
    browser.fill('comments', 'test@test.org')
    browser.fill('contact_number', 9999111111)
    captcha_value = get_captcha_value(browser.html)
    browser.fill('captcha_0', captcha_value)
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('Thank')

    # ---------------- testing auto fill name and email -----------------------
    f.create_usertype(slug='tutor', display_name='tutor')
    user = f.create_user()
    user.set_password('123123')
    user.save()
    url = base_url + '/accounts/login/'
    browser.visit(url)
    browser.fill('login', user.email)
    browser.fill('password', '123123')
    browser.find_by_css('[type=submit]')[0].click()
    assert len(outbox) == 1
    mail = outbox[0]
    confirm_link = re.findall(r'http.*/accounts/.*/', mail.body)
    assert confirm_link
    browser.visit(confirm_link[0])
    assert browser.title, "Confirm E-mail Address"
    browser.find_by_css('[type=submit]')[0].click()
    url = base_url + '/contact/'
    browser.visit(url)
    name = browser.find_by_id('id_name').value
    assert name == user.first_name + " " + user.last_name
    email = browser.find_by_id('id_email').value
    assert email == user.email

    # -------------------After logging out---------------
    url = base_url + '/accounts/logout/'
    browser.visit(url)
    assert 'Home | PythonExpress' in browser.title
    url = base_url + '/contact/'
    browser.visit(url)
    name = browser.find_by_id('id_name').value
    assert name == ''
    email = browser.find_by_id('id_email').value
    assert email == ''
