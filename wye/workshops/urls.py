from django.conf.urls import url
from .views import workshop_list, workshop_details, \
    workshop_create, WorkshopUpdate, WorkshopToggleActive, \
    WorkshopFeedbackView, WorkshopAction


urlpatterns = [
    url(r'^$', workshop_list, name="workshop_list"),
    url(r'^(?P<pk>\d+)/$', workshop_details, name="workshop_detail"),
    url(r'^create/$', workshop_create, name="workshop_create"),
    url(r'^update/(?P<pk>\d+)/$',
        WorkshopUpdate.as_view(), name="workshop_update"),
    url(r'^(?P<pk>\d+)/(?P<action>active|deactive)/$',
        WorkshopToggleActive.as_view(), name="workshop_toggle"),
    url(r'^(?P<pk>\d+)/(?P<action>accept|reject|hold|publish|decline)/$',
        WorkshopAction.as_view(), name="workshop_action"),
    url(r'^feedback/(?P<pk>\d+)/$',
        WorkshopFeedbackView.as_view(), name="workshop_feedback")
]
