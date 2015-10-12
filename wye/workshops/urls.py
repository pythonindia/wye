from django.conf.urls import url
from .views import WorkshopList, WorkshopDetail, \
    WorkshopCreate, WorkshopUpdate, WorkshopToggleActive, \
    WorkshopAssignMe

urlpatterns = [
    url(r'^$', WorkshopList.as_view(), name="workshop_list"),
    url(r'^(?P<pk>\d+)/$', WorkshopDetail.as_view(), name="workshop_detail"),
    url(r'^create/$', WorkshopCreate.as_view(), name="workshop_create"),
    url(r'^update/(?P<pk>\d+)/$',
        WorkshopUpdate.as_view(), name="workshop_update"),
    url(r'^(?P<action>[active,deactive]+)/(?P<pk>\d+)/$',
        WorkshopToggleActive.as_view(), name="workshop_toggle"),
    url(r'^presenter(?P<action>[opt-in,opt-out]+)/(?P<pk>\d+)/$',
        WorkshopAssignMe.as_view(), name="workshop_assignme")
]
