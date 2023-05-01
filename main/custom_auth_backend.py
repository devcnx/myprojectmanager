from django.contrib.auth.backends import ModelBackend
from django.shortcuts import redirect
from django.urls import reverse


class CustomAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Redirect non-superusers to the main app's index page upon successful login. This is used to prevent non-superusers from accessing the admin site and manipulating the database. If tthe user is a non-superuser, the session variable non_superuser_login is set to True.
        """
        user = super().authenticate(request, username, password, **kwargs)
        if user and not user.is_superuser:
            request.session['non_superuser_login'] = True
        return user
