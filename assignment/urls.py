from django.urls import path

from . import views

urlpatterns = [
    path('', views.AssignmentView.as_view(), name='assignment_list'),
    path('<uuid:assignment_uuid>/', views.AssignmentInfo.as_view(), name='assignment_info'),
    path('create/', views.CreateAssignment.as_view(), name='create_assignment'),
    path('<uuid:assignment_uuid>/update/', views.UpdateAssignment.as_view(), name='update_assignment'),
    path('<uuid:assignment_uuid>/delete/', views.DeleteAssignment.as_view(), name='delete_assignment'),
    path('<uuid:assignment_uuid>/download/<uuid:file_uuid>', views.AssignmentInfo.download, name='download_file')
]

