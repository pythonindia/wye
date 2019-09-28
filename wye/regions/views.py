import json
from braces import views
from django.http.response import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic

from wye.profiles.models import Profile
from . import forms, models


class RegionalListView(views.StaffuserRequiredMixin, generic.ListView):
    model = models.RegionalLead
    template_name = 'regions/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(
            RegionalListView, self).get_context_data(*args, **kwargs)
        context['state_list'] = models.State.objects.all()
        context['location_list'] = models.Location.objects.all()
        context['regional_list'] = models.RegionalLead.objects.all()
        context['user'] = self.request.user
        return context


class StateCreateView(views.StaffuserRequiredMixin, generic.CreateView):
    model = models.State
    form_class = forms.StateForm
    success_url = '/region/'
    template_name = 'regions/state/create.html'

    def post(self, request, *args, **kwargs):
        form = forms.StateForm(data=request.POST)
        if form.is_valid():
            form.modified_by = request.user
            form.created_by = request.user
            form.instance.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})


class StateEditView(views.StaffuserRequiredMixin, generic.UpdateView):
    model = models.State
    form_class = forms.StateForm
    success_url = '/region/'
    template_name = 'regions/state/edit.html'


class LocationCreateView(views.StaffuserRequiredMixin, generic.CreateView):
    model = models.Location
    form_class = forms.LocationForm
    success_url = '/region/'
    template_name = 'regions/location/create.html'

    def post(self, request, *args, **kwargs):
        form = forms.LocationForm(data=request.POST)
        if form.is_valid():
            form.modified_by = request.user
            form.created_by = request.user
            form.instance.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})


class LocationUpdateView(views.StaffuserRequiredMixin, generic.UpdateView):
    model = models.Location
    form_class = forms.LocationForm
    success_url = '/region/'
    template_name = 'regions/location/edit.html'


class RegionalLeadCreateView(views.StaffuserRequiredMixin, generic.CreateView):
    model = models.RegionalLead
    form_class = forms.RegionalLeadForm
    success_url = '/region/'
    template_name = 'regions/lead/create.html'

    def get_leads(self, request, l_id):
        lead_choices = Profile.objects.filter(
            location=l_id
        ).values_list('user__id', 'user__username')
        return HttpResponse(json.dumps(list(lead_choices)))

    def post(self, request, *args, **kwargs):
        if request.method == 'POST' and request.is_ajax:
            form = forms.RegionalLeadForm(data=request.POST)
            lead_choices = request.POST.get('leads')
            form.fields['leads'].choices = (lead_choices, lead_choices)

            if form.is_valid():
                form.modified_by = request.user
                form.created_by = request.user
                form.save()
                return HttpResponseRedirect(self.success_url)
            else:
                return render(request, self.template_name, {'form': form})


class RegionalLeadUpdateView(views.StaffuserRequiredMixin, generic.UpdateView):
    model = models.RegionalLead
    form_class = forms.RegionalLeadForm
    success_url = '/region/'
    template_name = 'regions/lead/edit.html'
