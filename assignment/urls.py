from django.urls import path

from . import views

urlpatterns = [
    path('', views.AssignmentView.as_view(), name='assignment_list'),
    path('create/', views.CreateAssignment.as_view(), name='create_assignment')
]
