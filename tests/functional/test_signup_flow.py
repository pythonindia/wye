import re


def test_signup_flow(base_url, browser, outbox):
    browser.visit(base_url)
    login_btn = browser.find_by_text('Log In')[0]
    login_btn.click()
    assert browser.is_element_present_by_text("Sign In")
    signup_btn = browser.find_by_text('Signup')[0]
    signup_btn.click()

    assert browser.is_element_present_by_text("Sign Up")
    browser.fill('username', 'john')
    browser.fill('email', 'john@example.com')
    browser.fill('password1', '123123')
    browser.fill('password2', '123123')
    submit_btn = browser.find_by_css('button[type=submit]')[0]
    submit_btn.click()

    # Email
    assert len(outbox) == 1
    mail = outbox[0]
    assert mail.to == ['john@example.com']
    confirm_link = re.findall(r'http.*/confirm-email/.*/', mail.body)
    assert confirm_link
    browser.visit(confirm_link[0])
    assert browser.is_text_present("john@example.com")
    confirm_btn = browser.find_by_text('Confirm')[0]
    confirm_btn.click()
    assert browser.is_element_present_by_text("Sign In")
    browser.fill('login', 'john@example.com')
    browser.fill('password', '123123')
    submit_btn = browser.find_by_css('button[type=submit]')[0]
    submit_btn.click()

    logout_btn = browser.find_by_text("Logout")[0]
    assert logout_btn
    assert not logout_btn.visible
    submit_btn = browser.find_by_css('.dropdown-toggle')[0].click()
    assert logout_btn.visible
