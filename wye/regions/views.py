from django.http import HttpResponseForbidden
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic

from braces import views

from . import forms
from . import models


class RegionalListView(views.LoginRequiredMixin, generic.ListView):
    model = models.RegionalLead
    template_name = 'regions/index.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseForbidden("Not Admin Member")
        return super(RegionalListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(
            RegionalListView, self).get_context_data(*args, **kwargs)
        context['state_list'] = models.State.objects.all()
        context['location_list'] = models.Location.objects.all()
        context['regional_list'] = models.RegionalLead.objects.all()
        context['user'] = self.request.user
        return context


class StateCreateView(views.LoginRequiredMixin, generic.CreateView):
    model = models.State
    form_class = forms.StateForm
    success_url = '/region/'
    template_name = 'regions/state/create.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseForbidden("Not Admin Member")
        return super(StateCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = forms.StateForm(data=request.POST)
        if form.is_valid():
            form.modified_by = request.user
            form.created_by = request.user
            form.instance.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})


class StateEditView(views.LoginRequiredMixin, generic.UpdateView):
    model = models.State
    form_class = forms.StateForm
    success_url = '/region/'
    template_name = 'regions/state/edit.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseForbidden("Not Admin Member")
        return super(StateEditView, self).dispatch(request, *args, **kwargs)


class LocationCreateView(views.LoginRequiredMixin, generic.CreateView):
    model = models.Location
    form_class = forms.LocationForm
    success_url = '/region/'
    template_name = 'regions/location/create.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseForbidden("Not Admin Member")
        return super(LocationCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = forms.LocationForm(data=request.POST)
        if form.is_valid():
            form.modified_by = request.user
            form.created_by = request.user
            form.instance.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})


class LocationUpdateView(views.LoginRequiredMixin, generic.UpdateView):
    model = models.Location
    form_class = forms.LocationForm
    success_url = '/region/'
    template_name = 'regions/location/edit.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseForbidden("Not Admin Member")
        return super(LocationUpdateView, self).dispatch(request, *args, **kwargs)


class RegionalLeadCreateView(views.LoginRequiredMixin, generic.CreateView):
    model = models.RegionalLead
    form_class = forms.RegionalLeadForm
    success_url = '/region/'
    template_name = 'regions/lead/create.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseForbidden("Not Admin Member")
        return super(RegionalLeadCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = forms.RegionalLeadForm(data=request.POST)
        if form.is_valid():
            form.modified_by = request.user
            form.created_by = request.user
            form.instance.save()

            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})


class RegionalLeadUpdateView(views.LoginRequiredMixin, generic.UpdateView):
    model = models.RegionalLead
    form_class = forms.RegionalLeadForm
    success_url = '/region/'
    template_name = 'regions/lead/edit.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseForbidden("Not Admin Member")
        return super(RegionalLeadUpdateView, self).dispatch(request, *args, **kwargs)
