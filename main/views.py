""" 
Views for the main app. 

The main app is the main app of the MyProjectManager application. It contains the 
index page and the dashboard page. The index page is the landing page for the application
and the dashboard page is the main page for the application. 
"""

from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from projects.models import Project
from work_orders.models import WorkOrder


class IndexView(LoginRequiredMixin, TemplateView):
    """
    View for the main app's index page. 

    The index page is the landing page for the application. It is the first page that the user will see whenever they
    visit the application. It's only accessible to logged in users. 

    """
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        """
        Gets the context data for the index page.
        
        The context data for the index page is the user that is currently logged in. The user is passed to the template
        so that the user's name can be displayed on the pages. 

        Returns: The context data for the index page. 
        """
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    """ 
    View for the main app's dashboard page.
    
    The dashboard page is the main page for the application. It is the page that the user will see if they click the 
    'View Dashboard' link from the landing page. It's only accessible to logged in users.
    """
    template_name = 'main/dashboard.html'

    def get_context_data(self, **kwargs):
        """ 
        Gets the context data for the dashboard page.
        
        The user that's logged in, work orders, open work orders, closed work orders, cancelled work orders, projects, 
        recently closed work orders (last 7 days) and recently cancelled work orders (last 7 days). 
        """
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['work_orders'] = WorkOrder.objects.all()
        context['open_work_orders'] = self.get_open_work_orders()
        context['closed_work_orders'] = self.get_closed_work_orders()
        context['cancelled_work_orders'] = self.get_cancelled_work_orders()
        context['projects'] = Project.objects.all()
        context['recently_closed_work_orders'] = self.get_recently_closed_work_orders()
        context['recently_cancelled_work_orders'] = self.get_recently_cancelled_work_orders()
        return context

    def get_open_work_orders(self):
        """ 
        Get all open work orders. 
        """
        return WorkOrder.objects.filter(work_order_status='Open')

    def get_closed_work_orders(self):
        """ 
        Get all closed work orders. 
        """
        return WorkOrder.objects.filter(work_order_status='Closed')

    def get_recently_closed_work_orders(self):
        """ 
        Get all closed work orders that were closed in the last 7 days.
        """
        seven_days_ago = datetime.now() - timedelta(days=7)
        return WorkOrder.objects.filter(work_order_status='Closed', last_updated_on__gte=seven_days_ago)

    def get_cancelled_work_orders(self):
        """ 
        Get all cancelled work orders. 
        """
        return WorkOrder.objects.filter(work_order_status='Cancelled')

    def get_recently_cancelled_work_orders(self):
        """ 
        Get recently cancelled work orders.
        """
        seven_days_ago = datetime.now() - timedelta(days=7)
        return WorkOrder.objects.filter(work_order_status='Cancelled', last_updated_on__gte=seven_days_ago)

    def handle_no_permission(self):
        """ 
        Redirects the user to the admin page if they don't have permission to view the dashboard page.
        """
        return redirect(reverse_lazy('admin:index'))
