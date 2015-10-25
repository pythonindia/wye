from django.conf.urls import url
from .views import WorkshopList, WorkshopDetail, \
    WorkshopCreate, WorkshopUpdate, WorkshopToggleActive, \
    WorkshopAssignMe, WorkshopFeedBackCreate


urlpatterns = [
    url(r'^$', WorkshopList.as_view(), name="workshop_list"),
    url(r'^(?P<pk>\d+)/$', WorkshopDetail.as_view(), name="workshop_detail"),
    url(r'^create/$', WorkshopCreate.as_view(), name="workshop_create"),
    url(r'^update/(?P<pk>\d+)/$',
        WorkshopUpdate.as_view(), name="workshop_update"),
    url(r'^(?P<pk>\d+)/(?P<action>active|deactive)/$',
        WorkshopToggleActive.as_view(), name="workshop_toggle"),
    url(r'^(?P<pk>\d+)/(?P<action>opt-in|opt-out)/$',
        WorkshopAssignMe.as_view(), name="workshop_assignme"),
    url(r'^feedback/(?P<pk>\d+)/$', WorkshopFeedBackCreate.as_view(), name="workshop_feedback"),
]
