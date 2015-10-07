from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from . import forms, models


# Create your views here.
def registration(request):
    template = loader.get_template('auth/signup.html')
    redirect_next = request.GET.get('next', '')
    redirect_url = redirect_next
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            email = request.POST.get('username')
            first_name = request.POST.get('firstname', '')
            last_name = request.POST.get('lastname', '')
            mobile = request.POST.get('mobile', '')
            password = request.POST.get('password', '')
            u = User(username=email, email=email,
                     first_name=first_name,
                     last_name=last_name,
                     is_active=True,
                     )
            u.set_password(password)
            u.save()
            p = models.Profile(user=u, mobile=mobile)
            p.save()
            if not redirect_url:
                redirect_url = '/'
            return HttpResponseRedirect(redirect_url)
    else:
        form = forms.SignupForm()
    context = RequestContext(request,
                             dict(
                                 form=form,
                                 redirect_url=redirect_url,
                                 next=redirect_next))
    return HttpResponse(template.render(context))


def login(request):
    template = loader.get_template('auth/login.html')
    redirect_next = request.GET.get('next', '')
    redirect_url = redirect_next
    if request.method == 'POST':
        form = forms.UserAuthenticationForm(None, request.POST)
        print(form.is_valid())
        print(form.errors)
        print(form.error_messages)
        if form.is_valid():
            user = authenticate(
                username=request.POST.get('username'),
                password=request.POST.get('password'))
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    if not redirect_url:
                        redirect_url = '/'
                    return HttpResponseRedirect(redirect_url)
                else:
                    message = 'Your account has been disabled!'
            else:
                message = 'Your username and password were incorrect.'
            # django_login(request, form.user_cache)
            # request.session['username'] = form.user_cache
            if not redirect_url:
                redirect_url = '/'
            return HttpResponseRedirect(redirect_url)
        else:
            message = form.errors.as_text().replace(
                '*', '').replace('__all__', '')
            message = message.replace('Email:', '')

        if redirect_url:
            redirect_url = '?next=%s&message=%s&% s' % (
                redirect_url, message, redirect_url)
        else:
            redirect_url = '?message=%s&% s' % (message, redirect_url)
        return HttpResponseRedirect(redirect_url)
    else:
        form = forms.UserAuthenticationForm()
    context = RequestContext(request,
                             dict(
                                 form=form,
                                 redirect_url=redirect_url,
                                 next=redirect_next))
    return HttpResponse(template.render(context))


def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/')


def profile(request):
    pass
