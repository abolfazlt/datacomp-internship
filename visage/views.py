from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Min, Count, Q
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from authentication.models import Token
from visage.models import Submission, Problem, Competition


@login_required
def submissions(request):
    if request.method == 'GET':
        context = {
            'submissions': Submission.objects.filter(user=request.user).order_by('-timestamp')
        }
        return render(request, 'submissions.html', context)
    else:
        return HttpResponseBadRequest('Unsupported method!')


def leader_board(request):
    if request.method == 'GET':
        context = {
            'submissions': User.objects.annotate(
                count=Count('submission', filter=Q(submission__is_final=True)),
                error=Min('submission__error', filter=Q(submission__is_final=True))
            ).values('username', 'error', 'count').filter(error__isnull=False, count__gt=0).order_by('error')
        }
        return render(request, 'leader_board.html', context)
    else:
        return HttpResponseBadRequest('Unsupported method!')


def competition(request):
    if request.method == 'GET':
        context = {
            'competitions': Competition.objects.order_by('id')
        }
        return render(request, 'competition.html', context)
    else:
        return HttpResponseBadRequest('Unsupported method!')


@login_required
def problem(request):
    if request.method == 'GET':
        context = {
            'problem': Problem.objects.order_by('id').last()
        }
        return render(request, 'problem.html', context)
    else:
        return HttpResponseBadRequest('Unsupported method!')


@csrf_exempt
def submit(request):
    if request.method == 'POST':
        if 'token' in request.POST:
            token = Token.objects.filter(uuid=request.POST['token'], active=True).first()
            if token is not None:
                if 'final' in request.POST:
                    final = request.POST['final'] == 'True'
                    if 'file' in request.FILES:
                        last_day_subs = Submission.objects.filter(
                            user=token.user, status__in='SPJ', timestamp__gte=datetime.now().date(), is_final=final
                        ).count()
                        if last_day_subs < 10 - (int(final) * 5):
                            p = Problem.objects.order_by('id').last()
                            Submission.objects.create(
                                user=token.user, problem=p, file=request.FILES['file'], is_final=final
                            )
                            return HttpResponse('Submitted!')
                        else:
                            return HttpResponseNotAllowed('Submission count per day exceeded!')
                    else:
                        return HttpResponseBadRequest('Missing File!')
                else:
                    return HttpResponseBadRequest('Missing Final!')
            else:
                return HttpResponseBadRequest('Invalid Token!')
        else:
            return HttpResponseBadRequest('Missing Token!')
    else:
        return HttpResponseBadRequest('Unsupported method!')


def download(request):
    if request.method == 'GET':
        return HttpResponse(Problem.objects.order_by('id').last().data.file.read(), content_type='application/zip')
    else:
        return HttpResponseBadRequest('Unsupported method!')
