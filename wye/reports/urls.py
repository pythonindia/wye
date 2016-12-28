from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^workshops_csv/$', views.get_tutor_college_poc_csv,
        name="workshop-csv"),
    url(r'^$', views.index, name="home"),

]
