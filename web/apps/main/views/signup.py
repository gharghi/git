from django.contrib.auth.decorators import login_required
import requests
from rest_framework.utils import json
from web.apps.jwt_store.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib import messages
from web.apps.main.forms.sign_up_form import SignUpForm
from web.apps.main.tokens.tokens import account_activation_token
from django.conf import settings


@login_required
def home(request):
    return render(request, 'registration/login.html')


def signup(request):
    if request.method == "GET":
        return render(request, 'registration/signup.html')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        try:
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                data = {
                    'email': form.instance.email,
                    'username': form.instance.username,
                    'password': request.POST['password1'],
                    'name': form.instance.first_name + ' ' + form.instance.last_name
                }
                create_git_user(data)
                current_site = get_current_site(request)
                subject = 'فعال سازی حساب Gitlabs'
                message = render_to_string('registration/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message)
                messages.success(request,'یک ایمیل حاوی کد فعال سازی برای شما ارسال شد.')
                return redirect('login')
            else:
                messages.error(request, form.errors)
                return redirect('signup')
        except Exception as e:
            messages.error(request,e)
            return redirect('signup')

    else:
        form = SignUpForm()
        return render(request, 'registration/login.html', {'form': form})



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        # login(request, user)
        messages.success(request, 'حساب شما فعال شد. لطفا به سامانه وارد شوید.')
        return redirect('login')
    else:
        messages.error(request, 'در فعال سازی مشکلی پیش آمده است. لطفا با پشتیبانی تماس بگیرید.')
        return redirect('login')


def create_git_user(data):
    params = {
               'email': data['email'],
               'username': data['username'],
               'password': data['password'],
               'name': data['name'],
               'projects_limit': str(settings.PROJECTS_LIMIT),
    }
    headers = {
        'Private-Token': settings.TOKEN,
    }
    r = requests.post(settings.GIT_URL +  'users', headers=headers, params=params, verify=False)
    j = json.loads(r.text)
    print(json.dumps(j, indent=4))
    return True