from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, include, reverse


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('visage:submissions'))
    else:
        return HttpResponseRedirect(reverse('authentication:login'))


urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('auth/', include(('authentication.urls', 'authentication'))),
    path('visage/', include(('visage.urls', 'visage'))),
]
