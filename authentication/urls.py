from django.urls import path

from authentication import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('verify/<uuid:uuid>/', views.verify, name='verify'),
]
