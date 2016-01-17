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
        user_profile, created = Profile.objects.get_or_create(
            user__id=self.request.user.id)
        if not user_profile.get_user_type:
            return redirect('profiles:profile-edit', slug=request.user.username)
        return super(OrganisationList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Organisation.objects.filter(active=True)

    def get_context_data(self, *args, **kwargs):
        context = super(OrganisationList, self).get_context_data(
            *args, **kwargs)
        if Profile.is_organiser(self.request.user):
            context['org_created_list'] = self.get_queryset().filter(
                created_by=self.request.user)
            context['org_belongs_list'] = self.get_queryset().exclude(
                created_by=self.request.user).filter(
                user=self.request.user)
        elif Profile.is_regional_lead(self.request.user):
            regions = RegionalLead.objects.filter(leads=self.request.user)
            context['regional_org_list'] = self.get_queryset().filter(
                location__id__in=[x.location.id for x in regions])
        context['user'] = self.request.user
        # need to improve the part
        context['is_not_tutor'] = False
        # as user can be tutor and regional lead hence we need to verify like
        # this
        if (Profile.is_regional_lead(self.request.user) or
                Profile.is_organiser(self.request.user) or
                Profile.is_admin(self.request.user)):
            context['is_not_tutor'] = True
        return context


class OrganisationCreate(views.LoginRequiredMixin, generic.CreateView):
    model = Organisation
    form_class = OrganisationForm
    template_name = 'organisation/create.html'
    success_url = reverse_lazy('organisations:organisation_list')

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

            regional_lead = Profile.objects.filter(
                interested_locations=form.instance.location,
                usertype__slug='lead').values_list('user__email', flat=True)
            send_email_to_id(subject,
                             body=email_body,
                             email_id=request.user.email,
                             text_body=text_body)

            send_email_to_list(subject,
                               body=email_body,
                               users_list=regional_lead,
                               text_body=text_body)

            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})


class OrganisationDetail(views.LoginRequiredMixin, generic.DetailView):
    model = Organisation
    template_name = 'organisation/detail.html'
    success_url = reverse_lazy('organisations:organisation_list')

    def get_queryset(self):
        return Organisation.objects.filter(
            user=self.request.user,
            id=self.kwargs['pk'])


class OrganisationUpdate(views.LoginRequiredMixin, generic.UpdateView):
    model = Organisation
    form_class = OrganisationForm
    template_name = 'organisation/edit.html'
    success_url = reverse_lazy('organisations:organisation_list')

    def get_object(self, queryset=None):
        return Organisation.objects.get(user=self.request.user, id=self.kwargs['pk'])


class OrganisationDeactive(views.CsrfExemptMixin,
                           views.LoginRequiredMixin,
                           views.JSONResponseMixin,
                           generic.UpdateView):
    model = Organisation
    fields = ('active', 'id')

    def get_object(self, queryset=None):
        return Organisation.objects.get(user=self.request.user,
                                        id=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = self.object.toggle_active(request.user, **kwargs)
        return self.render_json_response(response)
