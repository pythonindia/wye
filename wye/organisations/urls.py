from django.conf.urls import url
from .views import (
    OrganisationCreate, OrganisationDetail,
    OrganisationUpdate, OrganisationList,
    OrganisationDeactive, OrganisationMemberAdd)

urlpatterns = [
    url(r'^create/$', OrganisationCreate.as_view(),
        name="organisation_create"),
    url(r'^(?P<pk>\d+)/(?P<action>active|deactive)/$',
        OrganisationDeactive.as_view(), name="organisation_delete"),
    url(r'^(?P<pk>\d+)/edit/$',
        OrganisationUpdate.as_view(), name="organisation_update"),
    url(r'^(?P<pk>\d+)/member-add/$',
        OrganisationMemberAdd.as_view(), name="organisation_member_add"),
    url(r'^(?P<pk>\d+)/$', OrganisationDetail.as_view(),
        name="organisation_details"),
    url(r'^$', OrganisationList.as_view(), name="organisation_list"),

]
