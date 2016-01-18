# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView

from wye.base.views import HomePageView
from wye.profiles.views import UserDashboard, ContactFormView

urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^dashboard/$', UserDashboard.as_view(),
        name="dashboard"),
    url(r'^about/$', TemplateView.as_view(template_name='about.html',),
        name='about'),
    url(r'^contact/$', ContactFormView.as_view(),
        name='contact'),
    url(r'^thankyou/$', TemplateView.as_view(template_name='contact.html'),
        name='thankyou'),
    url(r'^workshops_info/$', TemplateView.as_view(
        template_name='workshops_info.html',),
        name='workshops_info'),
    url(r'^faq/$', TemplateView.as_view(template_name='faq.html',),
        name='faq'),
    url(r'^organisation/',
        include('wye.organisations.urls', namespace="organisations")),
    url(r'^workshop/',
        include('wye.workshops.urls', namespace="workshops")),
    url(r'^profile/',
        include('wye.profiles.urls', namespace="profiles")),
    url(r'^region/',
        include('wye.regions.urls', namespace="regions")),
    url(r'^$', HomePageView.as_view(),
        name='home-page'),
] + static(
    settings.STATIC_URL,
    document_root=settings.STATICFILES_DIRS) + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)
