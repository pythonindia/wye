from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.ProfileCreateView.as_view(),
        name="profile_create"),
    url(r'^(?P<slug>[a-zA-Z0-9]+)/$', views.ProfileView.as_view(),
        name='profile_page'),
    url(r'^dashboard$', views.UserDashboard.as_view(),
        name="dashboard"),
]
