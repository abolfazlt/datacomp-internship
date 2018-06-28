from django.urls import path

from visage import views

urlpatterns = [
    path('submissions/', views.submissions, name='submissions'),
    path('leader_board/', views.leader_board, name='leader_board'),
    path('problem/', views.problem, name='problem'),
    path('submit/', views.submit, name='submit'),
    path('download/', views.download, name='download'),
]