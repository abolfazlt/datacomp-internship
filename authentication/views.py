from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse

from authentication.models import Token


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('visage:submissions'))

    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        if 'username' not in request.POST:
            context = {
                'error': 'نام کاربری باید پر شود!'
            }
            return render(request, 'signup.html', context)
        else:
            username = request.POST['username']

        if 'email' not in request.POST:
            context = {
                'error': 'ایمیل باید پر شود!'
            }
            return render(request, 'signup.html', context)
        else:
            email = request.POST['email'].lower()

        if 'password' not in request.POST:
            context = {
                'error': 'رمز باید پر شود!'
            }
            return render(request, 'signup.html', context)
        else:
            password = request.POST['password']

        # TODO: For test drive :D
        if not (email.endswith('@cafebazaar.ir') or email.endswith('@divar.ir') or email.endswith('@resid.ir')):
            context = {
                'error': 'تنها امکان ثبت نام با ایمیل داخلی وجود دارد!'
            }
            return render(request, 'signup.html', context)

        if User.objects.filter(username=username).exists():
            context = {
                'error': 'کاربر با نام کاربری داده شده وجود دارد!'
            }
            return render(request, 'signup.html', context)
        elif User.objects.filter(email=email).exists():
            context = {
                'error': 'کاربر با ایمیل داده شده وجود دارد!'
            }
            return render(request, 'signup.html', context)
        else:
            user = User.objects.create_user(username, email, password)
            token = Token.objects.create(user=user)

            # TODO: Fix this!
            message = """
کد ارسال برای استفاده در مسابقه داخلی: {uuid}
لینک فعال سازی: http://79.175.132.14/auth/verify/{uuid}/
"""
            send_mail(
                'کد ارسال مسابقه داخلی کافه بازار', message.format(uuid=token.uuid),
                'datacomp@cafebazaar.ir', [email], fail_silently=False
            )

            return HttpResponseRedirect(reverse('authentication:login'))
    else:
        context = {
            'error': 'درخواست نامعتبر است!'
        }
        return render(request, 'signup.html', context)


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('visage:submissions'))

    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        if 'username' not in request.POST:
            context = {
                'error': 'نام کاربری باید پر شود!'
            }
            return render(request, 'login.html', context)
        else:
            username = request.POST['username']

        if 'password' not in request.POST:
            context = {
                'error': 'رمز باید پر شود!'
            }
            return render(request, 'login.html', context)
        else:
            password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.token.active:
                django_login(request, user)
                return HttpResponseRedirect(reverse('visage:submissions'))
            else:
                context = {
                    'error': 'ایمیل شما تایید نشده است!'
                }
                return render(request, 'login.html', context)
        else:
            context = {
                'error': 'کاربر با مشخصات داده شده وجود ندارد!'
            }
            return render(request, 'login.html', context)
    else:
        context = {
            'error': 'درخواست نامعتبر است!'
        }
        return render(request, 'login.html', context)


@login_required
def logout(request):
    if request.method == 'GET':
        django_logout(request)
        return HttpResponseRedirect(reverse('authentication:login'))
    else:
        return HttpResponseBadRequest('Unsupported method!')


def verify(request, uuid):
    if request.method == 'GET':
        token = Token.objects.filter(uuid=uuid, active=False).first()
        if token is not None:
            token.active = True
            token.save()
        return HttpResponseRedirect(reverse('authentication:login'))
    else:
        return HttpResponseBadRequest('Unsupported method!')
