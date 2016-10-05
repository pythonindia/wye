from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<days>\d+)/$', views.index, name="report-index"),

]
