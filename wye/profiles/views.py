from django.views.generic import DetailView

from . import models


class ProfileView(DetailView):
    model = models.Profile
    template_name = 'profile/index.html'

    def get_context_data(self, *args, **kwargs):
        slug = self.kwargs['slug']
        self.object = models.Profile.objects.get(
            slug=slug)
        context = super(
            ProfileView, self).get_context_data(*args, **kwargs)
        return context
