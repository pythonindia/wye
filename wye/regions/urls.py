from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^lead/create/$', views.RegionalLeadCreateView.as_view(),
        name="lead-create"),
    url(r'^lead/(?P<pk>\d+)/edit/$', views.RegionalLeadUpdateView.as_view(),
        name="lead-update"),

    url(r'^state/create/$', views.StateCreateView.as_view(),
        name="state-create"),
    url(r'^state/(?P<pk>\d+)/edit/$', views.StateEditView.as_view(),
        name="state-update"),

    url(r'^location/create/$', views.LocationCreateView.as_view(),
        name="location-create"),
    url(r'^location/(?P<pk>\d+)/edit/$', views.LocationUpdateView.as_view(),
        name="organisation_update"),
    url(r'^$', views.RegionalListView.as_view(), name="regions-home-page")

]
