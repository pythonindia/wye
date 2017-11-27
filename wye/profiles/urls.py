from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<slug>[a-zA-Z0-9@._-]+)/$',
        views.profile_view, name='profile-page'),
    url(r'^(?P<slug>[a-zA-Z0-9@._-]+)/edit/$',
        views.ProfileEditView.as_view(), name='profile-edit'),
    url(r'^(?P<slug>[a-zA-Z0-9@._-]+)/deactivate/$',
        views.account_deactivate, name='account_deactivate')
]
