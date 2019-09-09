from django.conf.urls import url
from .views import (
    OrganisationCreate, OrganisationDetail,
    OrganisationUpdate, OrganisationList,
    OrganisationDeactive, OrganisationMemberAdd)

urlpatterns = [
    url(r'^create/$', OrganisationCreate.as_view(),
        name="organisation_create"),
    url(r'^(?P<pk>[0-9]+)/(?P<action>active|deactive)/$',
        OrganisationDeactive.as_view(), name="organisation_delete"),
    url(r'^(?P<pk>[0-9]+)/edit/$',
        OrganisationUpdate.as_view(), name="organisation_update"),
    url(r'^(?P<pk>[0-9]+)/member-add/$',
        OrganisationMemberAdd.as_view(), name="organisation_member_add"),
    url(r'^(?P<pk>[0-9]+)/$', OrganisationDetail.as_view(),
        name="organisation_details"),
    url(r'^$', OrganisationList.as_view(), name="organisation_list"),

]
