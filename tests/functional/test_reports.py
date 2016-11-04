import re
from .. import factories as f


def test_report_page(base_url, browser, outbox):
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

    location1 = f.create_locaiton(name='location1')
    poc_type = f.create_usertype(slug='poc', display_name='poc')
    user.profile.usertype.clear()
    user.profile.usertype.add(poc_type)
    user.profile.location = location1
    user.profile.save()
    user.save()

    url = base_url + '/reports/'+'10/'
    browser.fill('login', user.email)
    browser.fill('password', '123123')
    browser.find_by_css('[type=submit]')[0].click()
    browser.visit(url)

    user.is_staff = True
    user.save()
    browser.visit(url)
