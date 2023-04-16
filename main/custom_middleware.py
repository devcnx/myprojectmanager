from django.shortcuts import redirect
from django.urls import reverse


class NonSuperuserLoginMiddleware:
    """
    Redirect non-superusers to the main app's index page upon successful login.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated and not request.user.is_superuser:
            if request.session.get('non_superuser_login'):
                request.session.pop('non_superuser_login')
                return redirect('main:index')
        return response
