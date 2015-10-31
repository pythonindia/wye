from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import generic

from braces import views
from wye.profiles.models import Profile

from .forms import OrganisationForm
from .models import Organisation


class OrganisationList(views.LoginRequiredMixin, generic.ListView):
    model = Organisation
    template_name = 'organisation/list.html'

    def dispatch(self, request, *args, **kwargs):
        user_profile = Profile.objects.get(
            user__id=self.request.user.id)
        if not user_profile.get_user_type:
            return redirect('profiles:profile_create')
        return super(OrganisationList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Organisation.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(OrganisationList, self).get_context_data(
            *args, **kwargs)
        context['organsation_list'] = self.get_queryset()
        context['org_created_list'] = self.get_queryset().filter(
            created_by=self.request.user)
        context['org_belongs_list'] = self.get_queryset().exclude(
            created_by=self.request.user)
        context['user'] = self.request.user
        return context


class OrganisationCreate(views.LoginRequiredMixin, generic.CreateView):
    model = Organisation
    form_class = OrganisationForm
    template_name = 'organisation/create.html'
    success_url = reverse_lazy('home-page')

    def get_queryset(self):
        return Organisation.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        form = OrganisationForm(data=request.POST)
        if form.is_valid():
            form.modified_by = request.user
            form.created_by = request.user
            form.instance.save()
            form.instance.user.add(request.user)
            form.instance.save()
            # send email on new organisation created
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})


class OrganisationDetail(views.LoginRequiredMixin, generic.DetailView):
    model = Organisation
    template_name = 'organisation/detail.html'
    success_url = reverse_lazy('home-page')

    def get_queryset(self):
        return Organisation.objects.filter(user=self.request.user, id=self.kwargs['pk'])


class OrganisationUpdate(views.LoginRequiredMixin, generic.UpdateView):
    model = Organisation
    form_class = OrganisationForm
    template_name = 'organisation/edit.html'
    success_url = reverse_lazy('home-page')

    def get_object(self, queryset=None):
        return Organisation.objects.get(user=self.request.user, id=self.kwargs['pk'])

    def put(self, request, *args, **kwargs):
        self.object = self.object()
        form = OrganisationForm(data=request.POST)
        if form.is_valid():
            if kwargs['action'] == 'edit':
                self.object.modified_by = request.user
                self.object.save()
            # Need to test this part of code
            if kwargs['action'] == 'deactive':
                self.object.modified_by = request.user
                self.object.active = False
                self.object.save()
                # send email on new organisation created
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})
