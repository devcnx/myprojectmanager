from django.contrib.auth.backends import ModelBackend
from django.shortcuts import redirect 
from django.urls import reverse


class CustomAuthBackend(ModelBackend):
    """
    Override the default authentication backend. 

    Redirect non-superusers to the main app's index page upon successful login.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username, password, **kwargs)
        if user and not user.is_superuser:
            request.session['non_superuser_login'] = True
        return user
    