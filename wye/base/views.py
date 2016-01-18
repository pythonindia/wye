from django.views.generic import TemplateView

from wye.organisations.models import Organisation
from wye.profiles.models import Profile
from wye.workshops.models import Workshop

from .constants import WorkshopStatus


class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        organisationObj = Organisation.objects.filter(active=True)
        workshopObj = Workshop.objects.filter(is_active=True)
        context['organisation_registered_count'] = organisationObj.count()
        context['completed_workshop_count'] = workshopObj.filter(
            status=WorkshopStatus.COMPLETED).count()
        context['requested_workshop_count'] = workshopObj.count()
        context['tutor_registered_count'] = Profile.objects.filter(
            usertype__slug="tutor").count()
        return context
