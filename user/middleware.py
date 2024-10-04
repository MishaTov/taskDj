from django.shortcuts import redirect
from django.urls import reverse_lazy

from .auth import hexdigest


class FirstLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            registration_url = reverse_lazy('registration', kwargs={'email_hash': hexdigest(request.user.email)})
            if request.user.first_login and request.path != registration_url:
                return redirect(registration_url)
        return self.get_response(request)
