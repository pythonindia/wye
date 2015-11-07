from django.conf.urls import url
from .views import WorkshopList, WorkshopDetail, \
    WorkshopCreate, WorkshopUpdate, WorkshopToggleActive, \
    WorkshopFeedbackView, WorkshopAction


urlpatterns = [
    url(r'^$', WorkshopList.as_view(), name="workshop_list"),
    url(r'^(?P<pk>\d+)/$', WorkshopDetail.as_view(), name="workshop_detail"),
    url(r'^create/$', WorkshopCreate.as_view(), name="workshop_create"),
    url(r'^update/(?P<pk>\d+)/$',
        WorkshopUpdate.as_view(), name="workshop_update"),
    url(r'^(?P<pk>\d+)/(?P<action>active|deactive)/$',
        WorkshopToggleActive.as_view(), name="workshop_toggle"),
    url(r'^(?P<pk>\d+)/(?P<action>accept|reject|hold)/$',
        WorkshopAction.as_view(), name="workshop_action"),
    url(r'^feedback/(?P<pk>\d+)/$',
        WorkshopFeedbackView.as_view(), name="workshop_feedback")
]
