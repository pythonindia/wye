from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        return super(HomePageView, self).get_context_data(**kwargs)
