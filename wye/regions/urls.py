from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^lead/create/$', views.RegionalLeadCreateView.as_view(),
        name="lead-create"),
    url(r'^lead/(?P<pk>[0-9]+)/edit/$', views.RegionalLeadUpdateView.as_view(),
        name="lead-update"),
    url(r'^lead/get_leads/(?P<l_id>\w+)/$', views.RegionalLeadCreateView().get_leads, name='get_leads'),
    url(r'^state/create/$', views.StateCreateView.as_view(),
        name="state-create"),
    url(r'^state/(?P<pk>[0-9]+)/edit/$', views.StateEditView.as_view(),
        name="state-update"),

    url(r'^location/create/$', views.LocationCreateView.as_view(),
        name="location-create"),
    url(r'^location/(?P<pk>[0-9]+)/edit/$', views.LocationUpdateView.as_view(),
        name="location-update"),
    url(r'^$', views.RegionalListView.as_view(), name="regions-home-page")

]
