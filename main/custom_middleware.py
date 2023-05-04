from django.shortcuts import redirect
from django.urls import reverse


class NonSuperuserLoginMiddleware:
    """ 
    Determine if the user is a non-superuser and redirect them to the main app's
    index page upon successful login. This is used to prevent non-superusers from
    accessing the admin site and manipulating the database. If the user is a
    non-superuser, the session variable 'non_superuser_login' is set to True.
    """

    def __init__(self, get_response):
        """ 
        Initialize the middleware with the get_response parameter.
        """
        self.get_response = get_response

    def __call__(self, request):
        """ 
        Process the request and return the response. If the user is 
        authenticated and not a superuser, check if the session variable
        'non_superuser_login' is set. If it is set, pop it and redirect to the
        main:index page.
        """
        response = self.get_response(request)
        if request.user.is_authenticated and not request.user.is_superuser:
            if request.session.get('non_superuser_login'):
                request.session.pop('non_superuser_login')
                return redirect('main:index')
        return response
