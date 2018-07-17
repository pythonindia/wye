import uuid

from django.conf import settings
from django.conf.urls import patterns, url
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import redirect, render
from django.template import Context, loader
from django.views import generic

from braces import views
from django.http.response import HttpResponseRedirect
from wye.base.emailer_html import send_email_to_id, send_email_to_list
from wye.profiles.models import Profile, UserType
from wye.regions.models import RegionalLead

from .forms import (
    OrganisationForm, OrganisationMemberAddForm,
    UserRegistrationForm
)
from .models import Organisation, User


class OrganisationList(views.LoginRequiredMixin, generic.ListView):
    model = Organisation
    template_name = 'organisation/list.html'

    def dispatch(self, request, *args, **kwargs):
        user_profile = Profile.objects.get(
            user__id=self.request.user.id)
        if not user_profile.is_profile_filled:
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
        # context['is_not_tutor'] = False
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

    def dispatch(self, request, *args, **kwargs):
        user_profile = Profile.objects.get(
            user__id=self.request.user.id)
        if not user_profile.is_profile_filled:
            return redirect('profiles:profile-edit', slug=request.user.username)
        if not user_profile.can_create_organisation:
            msg = '''Exceed number of organisaiton registration.
                Use contact us form to connect to co-ordinators'''
            return render(request, 'error.html', {'message': msg})
        return super(OrganisationCreate, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = OrganisationForm(data=request.POST)
        if form.is_valid():
            form.instance.modified_by = request.user
            form.instance.created_by = request.user
            form.instance.save()
            form.instance.user.add(request.user)
            form.instance.save()
            user_profile = Profile.objects.get(
                user__id=self.request.user.id)
            if not ('poc' in user_profile.get_user_type):
                poc_type = UserType.objects.get(slug='poc')
                user_profile.usertype.add(poc_type)
                user_profile.save()

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
        org = Organisation.objects.get(user=self.request.user, id=self.kwargs['pk'])
        if org.created_by == self.request.user:
            return Organisation.objects.get(user=self.request.user, id=self.kwargs['pk'])
        else:
            self.template_name = "403.html"


class OrganisationMemberAdd(views.LoginRequiredMixin, generic.UpdateView):
    model = Organisation
    form_class = OrganisationMemberAddForm
    template_name = 'organisation/member-add.html'
    success_url = reverse_lazy('organisations:organisation_list')

    def get_username(self, email):
        """
        Returns a UUID-based 'random' and unique username.

        This is required data for user models with a username field.
        """
        uuid_str = str(uuid.uuid4())
        username = email.split("@")[0]
        uuid_str = uuid_str[:30 - len(username)]
        return username + uuid_str

    def get_token(self, user, **kwargs):
        """Returns a unique token for the given user"""
        return PasswordResetTokenGenerator().make_token(user)

    def get_urls(self):
        return patterns('',
                        url(r'^(?P<user_id>[0-9]+)-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
                            view=self.activate_view, name="invitation_register")
                        )

    def post(self, request, *args, **kwargs):
        form = OrganisationMemberAddForm(data=request.POST)
        if form.is_valid():
            existing_user = form.cleaned_data['existing_user']
            new_user = form.cleaned_data['new_user']

            org = Organisation.objects.get(id=self.kwargs['pk'])
            host = '{}://{}'.format(settings.SITE_PROTOCOL,
                                    request.META['HTTP_HOST'])

            context = {
                'full_name': '%s %s' % (request.user.first_name,
                                        request.user.last_name),
                'org_name': org.name,
                'host': host
            }

            if existing_user:
                # add user to organisation
                user = existing_user
                org.user.add(user)
                org.save()

                # set email user's name in context
                context['new_member_name'] = '%s %s' % (user.first_name,
                                                        user.last_name)
                email_context = Context(context)

                # send mail to user being added
                subject = "You are added in %s organisation" % (
                    org.location.name)
                email_body = loader.get_template(
                    'email_messages/organisation/to_new_member_existing.html').render(
                        email_context)
                text_body = loader.get_template(
                    'email_messages/organisation/to_new_member_existing.txt').render(email_context)

                send_email_to_id(subject,
                                 body=email_body,
                                 email_id=user.email,
                                 text_body=text_body)

            elif new_user:
                # generate a random password
                random_password = User.objects.make_random_password()

                # create a user with the email from form
                user = User(username=self.get_username(new_user),
                            email=new_user,
                            password=random_password)

                # user is inactive initialy
                user.is_active = False
                user.save()

                # add the user to organisation
                org.user.add(user.id)
                org.save()

                # set the email context, the token will be used to generate a unique varification
                # link
                token = self.get_token(user)

                context['new_member_name'] = '%s' % (user.email)
                context['token'] = token
                context['user'] = user
                email_context = Context(context)

                # set the meta
                subject = "[Python Express]:You are added in %s organisation" % (
                    org.location.name)
                email_body = loader.get_template(
                    'email_messages/organisation/to_new_member.html').render(email_context)
                text_body = loader.get_template(
                    'email_messages/organisation/to_new_member.txt').render(email_context)

                # send the mail to new user
                send_email_to_id(subject,
                                 body=email_body,
                                 email_id=new_user,
                                 text_body=text_body)

            # These mails will be sent in both cases.
            subject = "user %s %s added in %s organisation" % (
                user.first_name, user.last_name, org.location.name)
            email_body = loader.get_template(
                'email_messages/organisation/member_addition_to_user.html').render(
                    email_context)
            text_body = loader.get_template(
                'email_messages/organisation/member_addition_to_user.txt').render(
                    email_context)

            # send mail to the user who added the new member
            send_email_to_id(subject,
                             body=email_body,
                             email_id=request.user.email,
                             text_body=text_body)

            regional_lead = Profile.objects.filter(
                interested_locations=org.location,
                usertype__slug='lead').values_list('user__email', flat=True)

            email_body = loader.get_template(
                'email_messages/organisation/member_addition_to_lead.html').render(
                    email_context)
            text_body = loader.get_template(
                'email_messages/organisation/member_addition_to_lead.txt').render(
                    email_context)

            # send mail to the regional leads
            send_email_to_list(subject,
                               body=email_body,
                               users_list=regional_lead,
                               text_body=text_body)

            return HttpResponseRedirect(self.success_url)

        else:
            return render(request, self.template_name, {'form': form})


def activate_view(request, user_id, token):
    """
    View function that activates the given User by setting `is_active` to
    true if the provided information is verified.
    """
    try:
        user = User.objects.get(id=user_id, is_active=False)
    except(User.DoesNotExist):
        raise Http404("Your URL may have expired.")

    if not PasswordResetTokenGenerator().check_token(user, token):
        raise Http404("Your URL may have expired.")

    form = UserRegistrationForm(data=request.POST or None, instance=user)
    if form.is_valid():
        user.is_active = True
        user.username = form.cleaned_data['username']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect(reverse_lazy('organisations:organisation_list'))
    else:
        return render(request, 'organisation/register_form.html',
                      {'form': form})


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
