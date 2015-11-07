from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import Context, loader
from django.views import generic

from braces import views
from wye.base.emailer_html import send_email_to_id, send_email_to_list
from wye.profiles.models import Profile
from wye.regions.models import RegionalLead
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
        return Organisation.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(OrganisationList, self).get_context_data(
            *args, **kwargs)
        print(Profile.is_regional_lead(self.request.user))
        if Profile.is_organiser(self.request.user):
            context['org_created_list'] = self.get_queryset().filter(
                created_by=self.request.user)
            context['org_belongs_list'] = self.get_queryset().exclude(
                created_by=self.request.user)
        elif Profile.is_regional_lead(self.request.user):
            print("AM here")
            regions = RegionalLead.objects.filter(leads=self.request.user)
            print([x.location.id for x in regions])
            context['regional_org_list'] = self.get_queryset().filter(
                location__id__in=[x.location.id for x in regions])
        elif Profile.is_presenter(self.request.user):
            pass
        context['user'] = self.request.user
        context['is_not_tutor'] = True if Profile.is_regional_lead(
            self.request.user) else not Profile.is_presenter(self.request.user)
        return context


class OrganisationCreate(views.LoginRequiredMixin, generic.CreateView):
    model = Organisation
    form_class = OrganisationForm
    template_name = 'organisation/create.html'
    success_url = reverse_lazy('organisations:organisation_list')

    def get_queryset(self):
        return Organisation.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        form = OrganisationForm(data=request.POST)
        if form.is_valid():
            form.instance.modified_by = request.user
            form.instance.created_by = request.user
            form.instance.save()
            form.instance.user.add(request.user)
            form.instance.save()
            host = '{}://{}'.format(settings.SITE_PROTOCOL,
                                    request.META['HTTP_HOST'])
            email_context = Context({
                'full_name': '%s %s' % (request.user.first_name,
                                        request.user.last_name),
                'org_id': form.instance.id,
                'host': host

            })
            subject = "%s organisation for region %s is created" % (
                form.instance.name, form.instance.location.name)
            email_body = loader.get_template(
                'email_messages/organisation/new.html').render(email_context)
            text_body = loader.get_template(
                'email_messages/organisation/new.txt').render(email_context)

            try:

                send_email_to_id(
                    subject,
                    body=email_body,
                    email_id=request.user.email,
                    text_body=text_body)
            except Exception as e:
                print(e)
            try:
                regional_lead = Profile.objects.filter(
                    interested_locations=form.instance.location,
                    usertype__slug='lead').values_list('user__email', flat=True)
                send_email_to_list(
                    subject,
                    body=email_body,
                    users_list=regional_lead,
                    text_body=text_body)
            except Exception as e:
                print(e)
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})


class OrganisationDetail(views.LoginRequiredMixin, generic.DetailView):
    model = Organisation
    template_name = 'organisation/detail.html'
    success_url = reverse_lazy('organisations:organisation_list')

    def get_queryset(self):
        return Organisation.objects.filter(user=self.request.user, id=self.kwargs['pk'])


class OrganisationUpdate(views.LoginRequiredMixin, generic.UpdateView):
    model = Organisation
    form_class = OrganisationForm
    template_name = 'organisation/edit.html'
    success_url = reverse_lazy('organisations:organisation_list')

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
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})
