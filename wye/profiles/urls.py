from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dashboard$', views.UserDashboard.as_view(),
        name="dashboard"),
    url(r'^(?P<slug>[a-zA-Z0-9@.]+)/$',
        views.profile_view, name='profile-page'),
    url(r'^(?P<slug>[a-zA-Z0-9@.]+)/edit$',
        views.ProfileEditView.as_view(), name='profile-edit')
]
