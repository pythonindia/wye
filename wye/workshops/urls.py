from django.conf.urls import url
from .views import WorkshopList, WorkshopDetail, \
    WorkshopCreate, WorkshopUpdate, WorkshopDelete

urlpatterns = [
    url(r'^$', WorkshopList.as_view()),
    url(r'^(?P<pk>\d+)$', WorkshopDetail.as_view()),
    url(r'^create/(?P<pk>\d+)$', WorkshopCreate.as_view()),
    url(r'^update/(?P<pk>\d+)$', WorkshopUpdate.as_view()),
    url(r'^delete/(?P<pk>\d+)$', WorkshopDelete.as_view()),
]
