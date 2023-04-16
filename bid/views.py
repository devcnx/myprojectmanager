from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from labor.models import LaborHours
from travel.models import TravelHours, TravelExpense
from .forms import BidForm, BidLaborHoursFormSet, BidLaborHoursForm, BidTravelHoursFormSet, BidTravelHoursForm, BidTravelExpenseFormSet, BidTravelExpenseForm
from .models import Bid


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'bid/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['bids'] = self.get_queryset()
        context['bids_draft'] = self.get_bids_by_status('Draft')
        context['bids_approved'] = self.get_bids_by_status(
            'Approved (Internally)')
        context['bids_submitted'] = self.get_bids_by_status(
            'Submitted to Customer')
        context['bids_awarded'] = self.get_bids_by_status('Awarded')
        context['bids_lost'] = self.get_bids_by_status('Lost')
        context['bids_no_bid'] = self.get_bids_by_status('No Bid')
        context['site_count'] = self.get_bid_project_sites_count()
        return context

    def get_queryset(self):
        return Bid.objects.all()

    def get_bids_by_status(self, status):
        return Bid.objects.filter(bid_status=status)

    def get_bid_project_sites_count(self):
        for bid in self.get_queryset():
            # Get the project.
            project = bid.bid_project
            # Get the sites for the project.
            project_sites_count = project.project_sites.count()
            # Return the count.
            return project_sites_count


class BidDetailView(LoginRequiredMixin, TemplateView):
    model = Bid
    template_name = 'bid/bid_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['bid'] = self.get_bid()
        context['bid_form'] = BidForm(instance=self.get_bid())

        labor_hours_initial = [
            {
                'labor_id': lh.labor_id,
                'labor_type': lh.labor_type,
                'labor_rate': lh.labor_rate,
                'labor_hours_quantity': lh.labor_hours_quantity,
                'labor_hours': lh.labor_hours,
            } for lh in self.get_bid().bid_labor_hours.all()
        ]
        context['labor_hours_formset'] = BidLaborHoursFormSet(
            prefix='labor_hours', initial=labor_hours_initial)

        travel_hours_initial = [
            {
                'travel_id': th.travel_id,
                'travel_type': th.travel_type,
                'travel_rate': th.travel_rate,
                'travel_hours_quantity': th.travel_hours_quantity,
                'travel_hours': th.travel_hours,
            } for th in self.get_bid().bid_travel_hours.all()
        ]
        context['travel_hours_formset'] = BidTravelHoursFormSet(
            prefix='travel_hours', initial=travel_hours_initial)

        travel_expense_initial = [
            {
                'travel_expense_id': te.travel_expense_id,
                'expense_type': te.expense_type,
                'expense_quantity': te.expense_quantity,
                'expense_amount': te.expense_amount,
            } for te in self.get_bid().bid_travel_expenses.all()
        ]
        context['travel_expense_formset'] = BidTravelExpenseFormSet(
            prefix='travel_expense', initial=travel_expense_initial)

        return context

    def get_bid(self):
        return Bid.objects.get(pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        bid = self.get_bid()
        bid_form = BidForm(request.POST, instance=bid)
        labor_hours_formset = BidLaborHoursFormSet(
            request.POST, prefix='labor_hours')
        travel_hours_formset = BidTravelHoursFormSet(
            request.POST, prefix='travel_hours')
        travel_expense_formset = BidTravelExpenseFormSet(
            request.POST, prefix='travel_expense')

        if bid_form.is_valid() and labor_hours_formset.is_valid() and travel_hours_formset.is_valid() and travel_expense_formset.is_valid():
            bid_form.instance.last_updated_by = request.user
            bid_form.save()

            for form in labor_hours_formset:
                labor_hours_data = form.cleaned_data
                labor_id = labor_hours_data.get('labor_id')
                if labor_id:
                    labor_hours = LaborHours.objects.get(pk=labor_id)
                    if form.cleaned_data.get('can_delete'):
                        labor_hours.delete()
                        continue
                else:
                    labor_hours = LaborHours()

                if form.is_valid() and labor_hours_data:
                    labor_hours.labor_type = labor_hours_data['labor_type']
                    labor_hours.labor_rate = labor_hours_data['labor_rate']
                    labor_hours.labor_hours_quantity = labor_hours_data['labor_hours_quantity']
                    labor_hours.labor_hours = labor_hours_data['labor_hours']
                    labor_hours.save()
                    bid.bid_labor_hours.add(labor_hours)

            for form in travel_hours_formset:
                travel_hours_data = form.cleaned_data
                travel_id = travel_hours_data.get('travel_id')
                if travel_id:
                    travel_hours = TravelHours.objects.get(pk=travel_id)
                    if form.cleaned_data.get('can_delete'):
                        travel_hours.delete()
                        continue
                else:
                    travel_hours = TravelHours()

                if form.is_valid() and travel_hours_data:
                    travel_hours.travel_type = travel_hours_data['travel_type']
                    travel_hours.travel_rate = travel_hours_data['travel_rate']
                    travel_hours.travel_hours_quantity = travel_hours_data['travel_hours_quantity']
                    travel_hours.travel_hours = travel_hours_data['travel_hours']
                    travel_hours.save()
                    bid.bid_travel_hours.add(travel_hours)

            for form in travel_expense_formset:
                travel_expense_data = form.cleaned_data
                travel_expense_id = travel_expense_data.get(
                    'travel_expense_id')
                if travel_expense_id:
                    travel_expense = TravelExpense.objects.get(
                        pk=travel_expense_id)
                    if form.cleaned_data.get('can_delete'):
                        travel_expense.delete()
                        continue
                else:
                    travel_expense = TravelExpense()

                if form.is_valid() and travel_expense_data:
                    travel_expense.expense_type = travel_expense_data['expense_type']
                    travel_expense.expense_quantity = travel_expense_data['expense_quantity']
                    travel_expense.expense_amount = travel_expense_data['expense_amount']
                    travel_expense.save()
                    bid.bid_travel_expenses.add(travel_expense)

            return HttpResponseRedirect(reverse('bid:bid_details', args=[bid.pk]))
        else:
            context = self.get_context_data()
            context['bid_form'] = bid_form
            context['labor_hours_formset'] = labor_hours_formset
            context['travel_hours_formset'] = travel_hours_formset
            context['travel_expense_formset'] = travel_expense_formset
            return render(request, self.template_name, context)
