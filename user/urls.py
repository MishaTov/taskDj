from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.Login.as_view(), name='login_page'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('registration/<slug:email_hash>', views.CompleteRegistration.as_view(), name='registration')
]
