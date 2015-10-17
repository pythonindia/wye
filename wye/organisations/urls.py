from django.conf.urls import url
from .views import OrganisationCreate, OrganisationDetail

urlpatterns = [
    url(r'^create/$', OrganisationCreate.as_view(),
        name="organisation_create"),
    url(r'^(?P<pk>\d+)/$', OrganisationDetail.as_view(),
        name="organisation_details"),

]
