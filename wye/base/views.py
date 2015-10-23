from django.views.generic import TemplateView

from wye.organisations.models import Organisation
from wye.workshops.models import Workshop
from wye.profiles.models import Profile
from .constants import WorkshopStatus


class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['organisation_registered_count'] = Organisation.objects.filter(active=True).count()
        context['completed_workshop_count'] = Workshop.objects.filter(status=WorkshopStatus.COMPLETED).count()
        context['tutor_registered_count'] = Profile.objects.filter(usertype__slug="tutor").count()
        return context
