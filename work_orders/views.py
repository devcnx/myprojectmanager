from django.views.generic import DetailView
from .models import WorkOrder, WorkOrderTrip


class WorkOrderDetailView(DetailView):
    model = WorkOrder
    template_name = 'work_orders/work_order_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['work_order_trips'] = self.get_work_order_trips()
        return context

    def get_work_order_trips(self):
        return WorkOrderTrip.objects.filter(work_order=self.object)
