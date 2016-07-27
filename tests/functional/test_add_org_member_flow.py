import re
from .. import factories as f


def test_add_new_member_flow(base_url, browser, outbox):
    # ----------------- creating new user ------------------------
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

    # ----------------------add user type -------------------
    poc_type = f.create_usertype(slug='poc', display_name='poc')
    user.profile.usertype.add(poc_type)
    user.profile.location = location1
    user.profile.save()
    user.save()

    # -----------------------creating organisation ---------------------
    url = base_url + '/organisation/'
    browser.fill('login', user.email)
    browser.fill('password', '123123')
    browser.find_by_css('[type=submit]')[0].click()
    browser.visit(url)
    org_create_link = browser.find_by_text('Add Organisation')[0]
    assert org_create_link
    org_create_link.click()
    browser.select('organisation_type', 1)
    browser.fill('name', 'Org1')
    browser.fill('description', 'Description')
    browser.select('location', location1.id)
    browser.fill('organisation_role', 'Role1')
    browser.find_by_css('[type=submit]')[0].click()

    org = f.create_organisation(location=location1)
    org.user.add(user)
    org.save()

    # -------------------Adding member ------------------------
    # existing user
    browser.find_by_text('Org1')[0].click()

    # add to org
    browser.find_by_text('Add Users')[0].click()
    browser.fill('new_user', 'user@example.com')
    browser.find_by_css('[type=submit]')[0].click()
    org.user.add(user)
    org.save()

    # invite mail
    assert len(outbox) == 6
    mail = outbox[3]
    invite_link = re.findall(r'http.*/invitation/.*/', mail.body)
    assert invite_link
    browser.visit(invite_link[0])
    # asserting if it's the signup page or not
    assert 'Signup' in browser.title

    # fill sign up form
    browser.fill('first_name', 'random')
    browser.fill('last_name', 'person')
    browser.fill('username', 'randomnessprevails')
    browser.fill('password', 'secretpassword')
    browser.fill('password_confirm', 'secretpassword')
    browser.find_by_css('[type=submit]')[0].click()

    # check user was added
    browser.find_by_text('Org1')[0].click()
    user_list = browser.find_by_css('.list-silent')
    assert 'user@example.com' in user_list[0].text

    # logout and login again to activate user
    logout_url = base_url + "/accounts/logout"
    browser.visit(logout_url)

    login_url = base_url + '/accounts/login/'
    browser.visit(login_url)
    browser.fill('login', 'user@example.com')
    browser.fill('password', 'secretpassword')
    browser.find_by_css('[type=submit]')[0].click()

    # confirmation email sent
    assert browser.is_text_present(
        'We have sent an e-mail to you for verification')
    assert len(outbox) == 7
    mail = outbox[6]

    activate_link = re.findall(r'http.*/accounts/confirm-email/.*/', mail.body)
    assert activate_link

    # confirmation dialogue
    browser.visit(activate_link[0])
    assert "Confirm E-mail Address" in browser.title
    browser.find_by_css('[type=submit]')[0].click()

    # login
    assert "Login" in browser.title
    browser.fill('login', 'user@example.com')
    browser.fill('password', 'secretpassword')
    browser.find_by_css('[type=submit]')[0].click()

    # edit profile
    assert browser.is_text_present("Dashboard")

    poc_type = f.create_usertype(slug='dummy', display_name='College POC')
    section1 = f.create_workshop_section(name='section1')
    location2 = f.create_locaiton(name='location2')

    url = base_url + '/profile/randomnessprevails/edit'
    browser.visit(url)

    browser.fill('mobile', '0812739120')
    # browser.select('usertype', poc_type.id)
    browser.select('interested_sections', section1.id)
    browser.select('interested_locations', location1.id)
    browser.select('location', location2.id)
    browser.find_by_css('[type=submit]')[0].click()

    assert browser.is_text_present('My Profile')
    assert browser.is_text_present('Graph')

    # Logging Out
    url = base_url + '/accounts/logout/'
    browser.visit(url)
    assert 'Home | PythonExpress' in browser.title


def test_add_existing_member_flow(base_url, browser, outbox):
    # ------------------creating new user ----------------------
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
    # ---------------------add user type -----------------------
    poc_type = f.create_usertype(slug='poc', display_name='poc')
    user.profile.usertype.add(poc_type)
    user.profile.location = location1
    user.profile.save()
    user.save()

    # -------------------creating organisation --------------------
    url = base_url + '/organisation/'
    browser.fill('login', user.email)
    browser.fill('password', '123123')
    browser.find_by_css('[type=submit]')[0].click()
    browser.visit(url)
    org_create_link = browser.find_by_text('Add Organisation')[0]
    assert org_create_link
    org_create_link.click()
    browser.select('organisation_type', 1)
    browser.fill('name', 'Org1')
    browser.fill('description', 'Description')
    browser.select('location', location1.id)
    browser.fill('organisation_role', 'Role1')
    browser.find_by_css('[type=submit]')[0].click()

    org = f.create_organisation(location=location1)
    org.user.add(user)
    org.save()

    # -------------- Adding member ------------------------

    # create user
    user2 = f.create_user(is_active=True)
    user2.set_password('123123')
    user2.save()
    user2.profile.usertype.add(poc_type)
    user2.save()

    # add to org
    browser.find_by_text('Org1')[0].click()
    browser.find_by_text('Add Users')[0].click()
    browser.select_by_text('existing_user', user2.username)
    browser.find_by_css('[type=submit]')[0].click()
    org.user.add(user2)
    org.save()

    # check user was added
    browser.find_by_text('Org1')[0].click()
    user_list = browser.find_by_css('.list-silent')
    assert user2.email in user_list[0].text

    assert 'Organisation | PythonExpress' in browser.title
