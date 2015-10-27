import re
from .. import factories as f


def test_forgot_password_flow(base_url, browser, outbox):
    user = f.UserFactory()

    # Forgot password link must be present on login page
    url = base_url + '/accounts/login/'
    browser.visit(url)
    forgot_pass_link = browser.find_by_text('Forgot Password?')[0]
    assert forgot_pass_link

    # When clicking on the link it should open a page and prompt for email
    forgot_pass_link.click()
    assert 'Password Reset' in browser.title
    browser.fill('email', 'no-existent-email@email.com')
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('The e-mail address is not assigned to any user account')
    assert len(outbox) == 0

    # Now, enter a valid email
    browser.fill('email', user.email)
    browser.find_by_css('button[type=submit]')[0].click()
    assert browser.is_text_present('We have sent you an e-mail.')
    assert len(outbox) == 1
    mail = outbox[0]
    reset_link = re.findall(r'http.*/reset/.*/', mail.body)
    assert reset_link

    browser.visit(reset_link[0])
    assert "Change Password" in browser.title
    assert browser.is_text_present('Change Password')
    browser.fill('password1', 'mynewpassword')
    browser.fill('password2', 'mynewpassword_wrong')
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('You must type the same password each time.')
    browser.fill('password1', 'mynewpassword')
    browser.fill('password2', 'mynewpassword')
    browser.find_by_css('[type=submit]')[0].click()
    assert browser.is_text_present('Your password is now changed.')
