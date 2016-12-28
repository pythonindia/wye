from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^export_workshops/$', views.get_tutor_college_poc_csv,
        name="workshop-csv"),
    url(r'^export_users/$', views.get_all_user_info,
        name="workshop-csv"),
    url(r'^$', views.index, name="home"),

]
