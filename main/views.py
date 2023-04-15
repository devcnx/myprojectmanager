from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from trips.models import Trip
from projects.models import Project
from work_orders.models import WorkOrder


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'main/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['work_orders'] = WorkOrder.objects.all()
        context['open_work_orders'] = self.get_open_work_orders()
        context['closed_work_orders'] = self.get_closed_work_orders()
        context['cancelled_work_orders'] = self.get_cancelled_work_orders()
        context['projects'] = Project.objects.all()
        context['work_order_trips_count'] = self.get_work_order_trips_count(
            context['work_orders'])

        return context

    def get_open_work_orders(self):
        return WorkOrder.objects.filter(work_order_status='Open')

    def get_closed_work_orders(self):
        return WorkOrder.objects.filter(work_order_status='Closed')

    def get_cancelled_work_orders(self):
        return WorkOrder.objects.filter(work_order_status='Cancelled')

    def handle_no_permission(self):
        return redirect(reverse_lazy('admin:index'))

    def get_work_order_trips_count(self, work_orders):
        trips = Trip.objects.filter(trip_id__in=work_orders)
        return trips.count()
