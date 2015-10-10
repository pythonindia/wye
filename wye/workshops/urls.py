from django.conf.urls import url
from .views import WorkshopList, WorkshopDetail, \
    WorkshopCreate, WorkshopUpdate, WorkshopDelete

urlpatterns = [
    url(r'^$', WorkshopList.as_view(), name="workshop_list"),
    url(r'^(?P<pk>\d+)$', WorkshopDetail.as_view(), name="workshop_detail"),
    url(r'^create$', WorkshopCreate.as_view(), name="workshop_create"),
    url(r'^update/(?P<pk>\d+)$', WorkshopUpdate.as_view(), name="workshop_update"),
    url(r'^delete/(?P<pk>\d+)$', WorkshopDelete.as_view(), name="workshop_delete"),
]
