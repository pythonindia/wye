# -*- coding: utf-8 -*-

# Third Party Stuff
from django.db.models import signals
import re
from . import factories as f


def signals_switch():
    pre_save = signals.pre_save.receivers
    post_save = signals.post_save.receivers

    def disconnect():
        signals.pre_save.receivers = []
        signals.post_save.receivers = []

    def reconnect():
        signals.pre_save.receivers = pre_save
        signals.post_save.receivers = post_save

    return disconnect, reconnect


disconnect_signals, reconnect_signals = signals_switch()


def create_user_verify_login(base_url, browser, outbox):
    user = f.create_user()
    user.set_password('123123')
    user.save()
    url = base_url + '/accounts/login/'
    browser.visit(url)
    browser.fill('login', user.email)
    browser.fill('password', '123123')
    browser.find_by_css('[type=submit]')[0].click()
    assert len(outbox) != 0
    mail = outbox[-1]
    confirm_link = re.findall(r'http.*/accounts/.*/', mail.body)
    assert confirm_link
    browser.visit(confirm_link[0])
    assert browser.title, "Confirm E-mail Address"
    browser.find_by_css('[type=submit]')[0].click()
    return user
