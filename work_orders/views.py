from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, CreateView
from .forms import WorkOrderTripForm
from .models import WorkOrder, WorkOrderTrip


class WorkOrderDetailView(DetailView):
    model = WorkOrder
    template_name = 'work_orders/work_order_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['work_order_trips'] = self.get_work_order_trips()
        return context

    def get_work_order_trips(self):
        return WorkOrderTrip.objects.filter(work_order=self.object)


def add_work_order_trip(request, pk):
    work_order = WorkOrder.objects.get(pk=pk)

    if request.method == 'POST':
        form = WorkOrderTripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.work_order = work_order
            trip.save()
            return redirect('work_orders:work_order_details', pk=work_order.pk)
    else:
        form = WorkOrderTripForm()
    return render(request, 'work_orders/add_work_order_trip.html', {'form': form, 'work_order': work_order})


class AddWorkOrderTripView(LoginRequiredMixin, CreateView):
    model = WorkOrderTrip
    template_name = 'work_orders/add_work_order_trip.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['work_order'] = WorkOrder.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.work_order = WorkOrder.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('work_orders:work_order_details', kwargs={'pk': self.kwargs['pk']})

    def get_initial(self):
        initial = super().get_initial()
        initial['work_order'] = WorkOrder.objects.get(pk=self.kwargs['pk'])
        initial['trip_start_date'] = datetime.now().date()
        initial['trip_start_time'] = datetime.now().time()
        initial['trip_end_date'] = datetime.now().date()
        initial['trip_end_time'] = datetime.now().time()
        initial['created_by'] = User.objects.get(pk=self.request.user.pk)
        initial['updated_by'] = User.objects.get(pk=self.request.user.pk)
        return initial

    def get_queryset(self):
        return super().get_queryset().filter(work_order__pk=self.kwargs['pk'])
