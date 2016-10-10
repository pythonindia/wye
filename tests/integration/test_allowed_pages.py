import pytest

from .. import factories as f

pytestmark = pytest.mark.django_db


public_pages = [
    '/',
    '/about/',
    '/faq/',
    '/accounts/login/',
    '/accounts/signup/',
    '/accounts/password/reset/',
]


staff_pages = [
    '/region/',
    '/region/lead/create/',
    '/region/location/create/',
    '/region/state/create/',
]


def test_public_pages(client):
    # These urls are publically accessible and their urls shouldn't change
    # with time.
    for page_url in public_pages:
        response = client.get(page_url)
        assert response.status_code == 200, 'Failed for %s' % page_url
        assert 'Log In' in str(response.content)


def test_staff_pages(client, settings):
    settings.SITE_VARIABLES['site_name'] = 'My Test Website'
    f.create_usertype(slug='tutor', display_name='tutor')
    normal_user = f.UserFactory(is_staff=False)
    staff_user = f.UserFactory(is_staff=True)

    for page_url in staff_pages:
        response = client.get(page_url)
        assert response.status_code == 302, 'Failed for %s' % page_url
        assert '/accounts/login?next=%s' % page_url in response['Location']

        # The page should render find after login
        if page_url in staff_pages:
            client.login(normal_user)
            assert response.status_code == 302, 'Failed for %s' % page_url
            assert '/accounts/login?next=%s' % page_url in response['Location']
            client.logout()

            client.login(staff_user)
            response = client.get(page_url)
            assert response.status_code == 200, 'Failed for %s' % page_url
            assert normal_user.get_full_name() in str(response.content)
            assert settings.SITE_VARIABLES[
                'site_name'] in str(response.content)
            client.logout()
        else:
            client.login(normal_user)
            response = client.get(page_url)
            assert response.status_code == 200, 'Failed for %s' % page_url
            assert normal_user.get_full_name() in str(response.content)
            assert settings.SITE_VARIABLES[
                'site_name'] in str(response.content)
            client.logout()


def test_orgnisation_pages(client, settings):
    f.create_usertype(slug='tutor', display_name='tutor')
    settings.SITE_VARIABLES['site_name'] = 'My Test Website'
    normal_user = f.UserFactory(is_staff=False)

    poc_type = f.create_usertype(slug='poc', display_name='poc')
    normal_user.profile.usertype.clear()
    normal_user.profile.usertype.add(poc_type)
    org = f.create_organisation()
    org.user.add(normal_user)
    org.save()
    normal_user.profile.location = org.location
    normal_user.profile.save()

    url_list = [
        '/organisation/',
        '/organisation/create/',
        '/organisation/{}/'.format(org.id),
        '/organisation/{}/edit/'.format(org.id),
    ]

    for page_url in url_list:
        client.login(normal_user)
        response = client.get(page_url)
        assert response.status_code == 200, 'Failed for %s' % page_url
        assert normal_user.get_full_name() in str(response.content)
        assert settings.SITE_VARIABLES[
            'site_name'] in str(response.content)
        client.logout()


def test_workshop_pages(client, settings):
    settings.SITE_VARIABLES['site_name'] = 'My Test Website'
    f.create_usertype(slug='tutor', display_name='tutor')
    poc_user = f.UserFactory(is_staff=False)
    poc_type = f.create_usertype(slug='poc', display_name='poc')
    poc_user.profile.usertype.clear()
    poc_user.profile.usertype.add(poc_type)
    org = f.create_organisation()
    org.user.add(poc_user)
    org.save()
    poc_user.profile.location = org.location
    poc_user.profile.save()
    workshop = f.create_workshop(requester=org)
    workshop.presenter.add(poc_user)
    workshop.save()

    url_list = [
        '/workshop/',
        '/workshop/create/',
        '/workshop/{}/'.format(workshop.id),
    ]

    for page_url in url_list:
        client.login(poc_user)
        response = client.get(page_url)
        assert response.status_code == 200, 'Failed for %s' % page_url
        assert poc_user.get_full_name() in str(response.content)
        assert settings.SITE_VARIABLES[
            'site_name'] in str(response.content)
        client.logout()
