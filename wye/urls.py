from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView


urlpatterns = [
    url(r'', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/$', TemplateView.as_view(template_name='about.html',),
        name='about'),
    url(r'^$', TemplateView.as_view(template_name='index.html',),
        name='home-page'),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

