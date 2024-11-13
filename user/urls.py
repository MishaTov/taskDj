from django.urls import path
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from . import views

urlpatterns = [
    path('login/', views.Login.as_view(), name='login_page'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('registration/<slug:email_hash>', views.CompleteRegistration.as_view(), name='registration'),
    path('password-reset/', views.PasswordResetView.as_view(
        template_name='user/password_reset_form.html',
        email_template_name='user/password_reset_email.html'),
         name='password_reset'),
    path('password-reset-done/', PasswordResetDoneView.as_view(
        template_name='user/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='user/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(
        template_name='user/password_reset_complete.html'),
         name='password_reset_complete'),
]
