from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.views import generic
# from io import BytesIO
# from reportlab.pdfgen import canvas
# from django.http import HttpResponse
from braces import views
from wye.organisations.models import Organisation
from wye.profiles.models import Profile
from wye.social.sites.twitter import send_tweet
from wye.base.views import (
    verify_user_profile)
# add_user_create_reset_password_link)
from wye.base.constants import WorkshopStatus
from .forms import (
    WorkshopForm,
    WorkshopEditForm,
    WorkshopFeedbackForm,
    WorkshopListForm,
    WorkshopVolunteer)
from .mixins import (
    WorkshopEmailMixin,
    WorkshopAccessMixin
)
from .utils import send_mail_to_group
from .models import Workshop, WorkshopFeedBack
# import xlrd


@login_required
@verify_user_profile
def workshop_list(request):
    template_name = 'workshops/workshop_list.html'
    user_profile, created = Profile.objects.get_or_create(
        user__id=request.user.id)
    if not user_profile.is_profile_filled:
        return redirect('profiles:profile-edit', slug=request.user.username)
    context_dict = {}
    workshop_list = Workshop.objects.filter(
        is_active=True, status__in=[
            WorkshopStatus.REQUESTED]).order_by('-expected_date', 'status')
    workshop_list = workshop_list.filter(
        requester__location__state__id__in=[
            x.id for x in request.user.profile.interested_states.all()]
    )

    location_list = request.GET.getlist("location")
    if location_list:
        workshop_list = workshop_list.filter(
            requester__location__id__in=location_list
        )

    workshop_level_list = request.GET.getlist("level")
    if workshop_level_list:
        workshop_list = workshop_list.filter(
            workshop_level__in=workshop_level_list
        )

    workshop_section_list = request.GET.getlist("section")
    if workshop_section_list:
        workshop_list = workshop_list.filter(
            workshop_section__id__in=workshop_section_list
        )

    context_dict['workshop_list'] = workshop_list
    context_dict['user'] = request.user
    # need to improve the part
    context_dict['is_not_tutor'] = False
    # as user can be tutor and regional lead hence we need to verify like
    # this
    if (Profile.is_regional_lead(request.user) or
            Profile.is_organiser(request.user) or
            Profile.is_admin(request.user)):
        context_dict['is_not_tutor'] = True

    context_dict['form'] = WorkshopListForm(user=request.user)

    return render(request, template_name, context_dict)


def workshop_details(request, pk):
    template_name = 'workshops/workshop_detail.html'
    workshop_obj = get_object_or_404(Workshop, id=pk)
    show_contact_flag = False
    display_edit_button = False
    user = request.user
    user_is_presenter = [u for u in workshop_obj.presenter.all() if user == u]
    user_is_requester = [
        u for u in workshop_obj.requester.user.all() if user == u]
    if (user_is_presenter or user_is_requester or
            user.is_superuser or (
                (not user.is_anonymous()) and Profile.is_coordinator(user))):
        show_contact_flag = True
    if (user_is_presenter):
        display_edit_button = True
    is_admin = True if user.is_superuser else False
    form = WorkshopVolunteer(initial={
        'number_of_volunteers': workshop_obj.number_of_volunteers or 0})

    context_dict = {
        'workshop': workshop_obj,
        'show_contact_flag': show_contact_flag,
        'display_edit_button': display_edit_button,
        'is_admin': is_admin,
        'form': form,
        'user': request.user
    }
    return render(request, template_name, context_dict)


@login_required
@verify_user_profile
def workshop_create(request):
    template_name = 'workshops/workshop_create.html'
    context_dict = {}
    if not Organisation.list_user_organisations(request.user).exists():
        msg = """
                To request workshop you need to create organisaiton.\n\n
                Please use organisation tab above to create your organisation
            """
        return render(request, 'error.html', {'message': msg})
    if request.method == 'GET':
        form = WorkshopForm(user=request.user)
        context_dict['form'] = form
        return render(request, template_name, context_dict)
    form = WorkshopForm(user=request.user, data=request.POST)
    if not form.is_valid():
        context_dict['form'] = form
        context_dict['errors'] = form.errors
        return render(request, template_name, context_dict)
    workshop = form.save()
    # domain = Site.objects.get_current().domain
    if workshop and workshop.id:
        context = {
            'workshop': workshop,
            'date': workshop.expected_date,
            'workshop_url': workshop.build_absolute_uri(
                reverse('workshops:workshop_detail', args=[workshop.pk]))
        }
        send_mail_to_group(context, workshop)
        send_tweet(context)
        success_url = reverse_lazy('workshops:workshop_list')
    return HttpResponseRedirect(success_url)


class WorkshopUpdate(views.LoginRequiredMixin, WorkshopAccessMixin,
                     generic.UpdateView):
    model = Workshop
    form_class = WorkshopEditForm
    template_name = 'workshops/workshop_update.html'

    def get_success_url(self):
        # pk = self.kwargs.get(self.pk_url_kwarg, None)
        self.success_url = reverse("workshops:workshop_list")
        return super(WorkshopUpdate, self).get_success_url()

    def get_initial(self):
        return {
            "requester": self.object.requester.name,
        }

    def get_form_kwargs(self):
        kwargs = super(WorkshopUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class WorkshopToggleActive(views.LoginRequiredMixin, views.CsrfExemptMixin,
                           views.JSONResponseMixin, WorkshopAccessMixin,
                           generic.UpdateView):
    model = Workshop
    fields = ('is_active', 'id')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = self.object.toggle_active(request.user, **kwargs)
        return self.render_json_response(response)


@login_required
def workshop_feedback_view(request, pk):
    context_dict = {}
    template_name = "workshops/workshop_feedback.html"
    context_dict['workshop'] = Workshop.objects.get(pk=pk)
    if request.method == 'POST':
        form = WorkshopFeedbackForm(
            data=request.POST, user=request.user, id=pk)
        if form.is_valid():
            WorkshopFeedBack.save_feedback(
                request.user, pk, **request.POST)
            success_url = reverse_lazy('workshops:workshop_list')
            return HttpResponseRedirect(success_url)
        context_dict['form'] = form
        context_dict['user'] = request.user
        return render(request, template_name, context_dict)
    else:
        context_dict['form'] = WorkshopFeedbackForm(
            user=request.user, id=pk)
    context_dict['user'] = request.user
    return render(request, template_name, context_dict)


class WorkshopAction(views.CsrfExemptMixin, views.LoginRequiredMixin,
                     views.JSONResponseMixin, WorkshopEmailMixin,
                     generic.UpdateView):

    model = Workshop
    email_dir = 'email_messages/workshop/assign_me/'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = self.object.manage_action(request.user, **kwargs)

        if response['status'] and response.get('notify') is not None:
            self.send_mail(request.user, response['assigned'])
            del response['notify']
        return self.render_json_response(response)

    def send_mail(self, user, assigned):
        """Send email to presenter and org users."""

        workshop = self.object
        context = {
            'presenter': True,
            'assigned': assigned,
            'date': workshop.expected_date,
            'presenter_name': user.username,
            'workshop_organization': workshop.requester,
            'workshop_url': self.request.build_absolute_uri(reverse(
                'workshops:workshop_detail', args=[workshop.pk]
            ))
        }
        # email to presenter and group
        self.send_mail_to_presenter(user, context)
        context['presenter'] = False
        send_mail_to_group(context, workshop, exclude_emails=[user.email])


@csrf_exempt
@login_required
def workshop_update_volunteer(request, pk):
    if request.GET:
        return JsonResponse({"items": range(1, 6)})

    if request.POST:
        volunteers = request.POST.get('number_of_volunteers')
        tutor_reimbursement_flag = request.POST.get('tutor_reimbursement_flag')
        comments = request.POST.get('comments')
        if volunteers.strip() not in ('', None):
            workshop_volunteer = Workshop.objects.filter(pk=pk)
            workshop_volunteer.update(number_of_volunteers=volunteers)
        if tutor_reimbursement_flag:
            workshop_volunteer.update(
                tutor_reimbursement_flag=tutor_reimbursement_flag)
        if comments:
            workshop_volunteer.update(comments=comments)
        return JsonResponse({
            "status": True,
            "msg": "Updated successfully"})
    return JsonResponse({"status": False, "msg": "Somthing went wrong"})


@csrf_exempt
@login_required
def workshop_accept_as_volunteer(request, pk):
    if request.method == 'POST':
        workshop = Workshop.objects.get(pk=pk)
        user = request.user

        if workshop.number_of_volunteers == 0:
            return JsonResponse({
                "status": False,
                "msg": "Volunteer not request for this workshop."})
        elif workshop.number_of_volunteers - workshop.volunteer.count() >= 1:
            # Check if already registered
            if user in workshop.volunteer.all():
                return JsonResponse({
                    "status": False,
                    "msg": "You are already registered as volunteer."})
            else:
                workshop.volunteer.add(user)
                return JsonResponse({
                    "status": True,
                    "msg": "Registered successfully."})
        else:
            return JsonResponse({
                "status": False,
                "msg": "Sorry, We have got required volunteers already"})
    return JsonResponse({"status": False, "msg": "Something went wrong"})


@csrf_exempt
@login_required
def workshop_opt_out_as_volunteer(request, pk):
    if request.method == 'POST':
        workshop = Workshop.objects.get(pk=pk)
        user = request.user

        if user in workshop.volunteer.all():
            # remove volunteer
            workshop.volunteer.remove(user)

            workshop.save()
            return JsonResponse({
                "status": True,
                "msg": "Opt-out successfully."})
        else:
            return JsonResponse({
                "status": False,
                "msg": "You are not registered as volunteer."})
    return JsonResponse({"status": False, "msg": "Something went wrong"})
