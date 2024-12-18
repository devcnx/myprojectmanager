import json
from bid.templatetags.bid_tags import get_material_description, get_manufacturer, get_manufacturer_number, format_unit_of_measure, multiply
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Case, When, IntegerField, Sum
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView

from equipment.models import Equipment
from labor.models import LaborHours
from materials.forms import MaterialForm
from materials.models import Material, MaterialVendor
from myprojectmanager.custom_json_encoder import CustomJSONEncoder
from projects.models import Project
from travel.models import TravelHours, TravelExpense
from .forms import BidForm, BidLaborHoursFormSet, BidLaborHoursForm, BidTravelHoursFormSet, BidTravelHoursForm, BidTravelExpenseFormSet, BidTravelExpenseForm, BidMaterialForm, BidEquipmentForm, BidEquipmentFormSet
from .models import Bid, BidMaterial, BidEquipment


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'bid/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['bids'] = self.get_queryset()
        context['bids_generated'] = self.get_bids_by_status('Generated')
        context['bids_additional'] = self.get_bids_by_status('Additional')
        context['bids_approved'] = self.get_bids_by_status(
            'Approved (Internally)')
        context['bids_submitted'] = self.get_bids_by_status(
            'Submitted to Customer')
        context['bids_awarded'] = self.get_bids_by_status('Awarded')
        context['bids_lost'] = self.get_bids_by_status('Lost')
        context['bids_no_bid'] = self.get_bids_by_status('No Bid')
        return context

    def get_queryset(self):
        return Bid.objects.all()

    def get_bids_by_status(self, status):
        return Bid.objects.filter(bid_status=status)


class BidDetailView(LoginRequiredMixin, TemplateView):
    model = Bid, LaborHours, TravelHours, TravelExpense
    template_name = 'bid/bid_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['bid'] = self.get_bid()
        bid_form = BidForm(instance=self.get_bid())
        bid_form['bid_project'].field.readonly_fields = True
        context['bid_form'] = BidForm(instance=self.get_bid())
        context['bid_material_form'] = BidMaterialForm()

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

        context['bid_materials'] = self.get_bid().bid_materials.all()

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
                    labor_hours = LaborHours.objects.get(labor_id=labor_id)
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
                expense_id = travel_expense_data.get('travel_expense_id')
                if expense_id:
                    travel_expense = TravelExpense.objects.get(pk=expense_id)
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

            bid.save()
            return HttpResponseRedirect(reverse('bid:bid_details', args=[bid.pk]))
        else:
            context = self.get_context_data()
            context['bid_form'] = bid_form
            context['bid_material_form'] = BidMaterialForm
            context['labor_hours_formset'] = labor_hours_formset
            context['travel_hours_formset'] = travel_hours_formset
            context['travel_expense_formset'] = travel_expense_formset
            return render(request, self.template_name, context)


class BidDetailsMaterialView(LoginRequiredMixin, TemplateView):
    template_name = 'bid/bid_details_material.html'

    def get_context_data(self, **kwargs):
        # Get the bid from the args passed from the bid detail view.
        # This is the bid that we are editing.
        bid = Bid.objects.get(pk=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['bid'] = bid
        bid_materials = bid.bid_materials.all()
        if bid_materials:
            context['bid_materials'] = bid_materials
        else:
            context['bid_materials'] = None

        context['bid_material_form'] = BidMaterialForm

        context['all_materials'] = self.get_all_materials()
        context['unique_manufacturers'] = self.get_unique_manufacturers()
        context['project_sites'] = self.get_project_sites()

        material_vendors = MaterialVendor.objects.select_related(
            'vendor').all()
        context['material_vendors'] = material_vendors
        context['price_extremes'] = self.find_material_price_extremes(
            material_vendors)
        context['bid_materials'] = self.get_bid_materials_data(bid)
        context['bid_materials_data_json'] = json.dumps(
            context['bid_materials'], cls=CustomJSONEncoder)

        # Get the UOMs for each bid material if it exists
        bid_material_uoms = {}
        for bid_material in bid_materials:
            bid_material_uoms[bid_material.material.material_id] = bid_material.unit_of_measure

        context['bid_material_uoms'] = bid_material_uoms

        bid_material_unit_prices = {}
        for bid_material in bid_materials:
            bid_material_unit_prices[bid_material.material.material_id] = bid_material.unit_price

        context['bid_material_unit_prices'] = bid_material_unit_prices

        context['total_cost'] = self.get_total_material_cost(bid_materials)

        # add_material_form = MaterialForm()
        # context['add_material_form'] = add_material_form

        return context

    def get_all_materials(self):
        return Material.objects.all()

    def get_total_material_cost(self, bid_materials):
        total_material_cost = 0
        for bid_material in bid_materials:
            total_material_cost += bid_material.quantity * bid_material.unit_price
        return total_material_cost

    def get_unique_manufacturers(self):
        return Material.get_unique_manufacturers()

    def get_project_sites(self):
        bid = Bid.objects.get(pk=self.kwargs['pk'])
        return bid.bid_project.project_sites.all()

    def find_material_price_extremes(self, material_vendors):
        price_extremes = {}
        for material_vendor in material_vendors:
            material_id = material_vendor.material_id
            if material_id not in price_extremes:
                price_extremes[material_id] = {
                    'min': float(material_vendor.vendor_unit_price),
                    'max': float(material_vendor.vendor_unit_price)
                }
            else:
                if material_vendor.vendor_unit_price < price_extremes[material_id]['min']:
                    price_extremes[material_id]['min'] = float(
                        material_vendor.vendor_unit_price)
                if material_vendor.vendor_unit_price > price_extremes[material_id]['max']:
                    price_extremes[material_id]['max'] = float(
                        material_vendor.vendor_unit_price)

        return price_extremes

    def get_bid_materials_data(self, bid):
        bid_materials = bid.bid_materials.all()
        bid_materials_data = []
        for bid_material in bid_materials:
            bid_materials_data.append({
                'material_id': bid_material.material.material_id,
                'quantity': bid_material.quantity,
                'unit_of_measure': bid_material.unit_of_measure,
                'unit_price': bid_material.unit_price,
            })
        return bid_materials_data

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        bid = Bid.objects.get(pk=self.kwargs['pk'])

        # Parse the bid materials data from the request body.
        bid_materials_data = json.loads(request.body)

        # Save the bid materials data to the database.
        for bid_material_data in bid_materials_data:
            material = Material.objects.get(
                material_id=bid_material_data['material_id'])
            quantity = bid_material_data['quantity']
            unit_of_measure = bid_material_data.get(
                'unit_of_measure', None)
            unit_price = bid_material_data.get('unit_price', None)

            # Check if there's already a BidMaterial instance.
            bid_material, created = BidMaterial.objects.get_or_create(
                material=material, bid=bid, defaults={
                    'quantity': quantity,
                    'unit_of_measure': unit_of_measure,
                    'unit_price': unit_price
                })

            # If the BidMaterial instance already exists, update the quantity.
            if not created:
                bid_material.quantity += quantity
                bid_material.unit_of_measure = unit_of_measure
                bid_material.save()

            # If the BidMaterial instance doesn't exist, create it.
            else:
                bid_material.save()
                bid.bid_materials.add(bid_material)

            bid.save()

        return JsonResponse({
            'status': 'success',
            'redirect_url': reverse('bid:bid_details_material', args=[bid.pk])
        })


def delete_bid_material(request, bid_id, material_id):
    bid = get_object_or_404(Bid, pk=bid_id)
    material = get_object_or_404(Material, pk=material_id)

    # Find the BidMaterial object associated with the bid and material.
    bid_material = get_object_or_404(BidMaterial, bid=bid, material=material)

    # Remove the BidMaterial object.
    bid.bid_materials.remove(bid_material)
    bid.save()

    bid_material.delete()

    return redirect('bid:bid_details_material', pk=bid_id)


class BidDetailsEquipmentView(LoginRequiredMixin, TemplateView):
    model = Bid, Equipment, BidEquipment
    template_name = 'bid/bid_details_equipment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bid = Bid.objects.get(pk=self.kwargs['pk'])
        context['bid'] = bid
        bid_equipment = bid.bid_equipment
        context['bid_equipment'] = bid_equipment

        bid_equipment = bid.bid_equipment.all()
        bid_equipment_initial = []
        for be in bid_equipment:
            bid_equipment_initial.append({
                'equipment': be.equipment,
                'quantity': be.quantity,
                'unit_price': be.unit_price,
                'start_date': be.start_date,
                'start_time': be.start_time,
                'end_date': be.end_date,
                'end_time': be.end_time,
            })
        context['bid_equipment_formset'] = BidEquipmentFormSet(
            prefix='bid_equipment', initial=bid_equipment_initial)

        return context

    def get_bid_equipment_data(self, bid):

        return bid_equipment_data

    def post(self, request, *args, **kwargs):
        bid = Bid.objects.get(pk=self.kwargs['pk'])
        bid_equipment_formset = BidEquipmentFormSet(
            request.POST, prefix='bid_equipment')

        if bid_equipment_formset.is_valid():
            bid.last_updated_by = request.user

            for form in bid_equipment_formset:
                bid_equipment_data = form.cleaned_data
                bid_equipment_id = bid_equipment_data.get('id')

                if bid_equipment_id:
                    bid_equipment = BidEquipment.objects.get(
                        pk=bid_equipment_id)
                    if form.cleaned_data.get('can_delete'):
                        bid.bid_equipment.remove(bid_equipment)
                        bid_equipment.delete()
                        continue
                else:
                    bid_equipment = BidEquipment()

                if form.is_valid() and bid_equipment_data:
                    bid_equipment.equipment = bid_equipment_data['equipment']
                    bid_equipment.quantity = bid_equipment_data['quantity']
                    bid_equipment.unit_price = bid_equipment_data['unit_price']
                    bid_equipment.start_date = bid_equipment_data['start_date']
                    bid_equipment.start_time = bid_equipment_data['start_time']
                    bid_equipment.end_date = bid_equipment_data['end_date']
                    bid_equipment.end_time = bid_equipment_data['end_time']
                    can_delete = bid_equipment_data.get('can_delete')
                    if can_delete:
                        bid_equipment.delete()
                    bid_equipment.save()
                    bid.bid_equipment.add(bid_equipment)

            bid.save()

            return HttpResponseRedirect(reverse('bid:bid_details_equipment', args=[bid.pk]))

        else:
            context = self.get_context_data()
            context['bid'] = bid
            context['bid_equipment_formset'] = bid_equipment_formset
            return render(request, self.template_name, context)


class BidSummaryView(LoginRequiredMixin, TemplateView):
    template_name = 'bid/bid_summary.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        bid = Bid.objects.get(pk=self.kwargs['pk'])
        context['bid'] = bid
        context['bid_project'] = bid.bid_project
        bid_labor_hours = bid.bid_labor_hours.all()
        context['bid_labor_hours'] = bid_labor_hours
        bid_travel_hours = bid.bid_travel_hours.all()
        context['bid_travel_hours'] = bid_travel_hours
        bid_travel_expenses = bid.bid_travel_expenses.all()
        context['bid_travel_expenses'] = bid_travel_expenses
        bid_materials = bid.bid_materials.all()
        context['bid_materials'] = bid_materials
        bid_equiment = bid.bid_equipment.all()
        context['bid_equipment'] = bid_equiment

        labor_totals = self.get_labor_totals(bid_labor_hours)
        context['labor_totals'] = labor_totals

        travel_totals = self.get_travel_hours(bid_travel_hours)
        context['travel_totals'] = travel_totals

        expense_totals = self.get_travel_expenses(bid_travel_expenses)
        context['expense_totals'] = expense_totals

        material_totals = self.get_material_totals(bid_materials)
        context['material_totals'] = material_totals

        equiment_totals = self.get_equipment_totals(bid.bid_equipment.all())
        context['equipment_totals'] = equiment_totals
        return context

    def get_labor_totals(self, bid_labor_hours):
        labor_total = 0
        for labor in bid_labor_hours:
            quantity = labor.labor_hours_quantity
            hours = labor.labor_hours
            rate = labor.labor_rate
            labor_total += quantity * hours * rate.rate_amount
        return labor_total

    def get_travel_hours(self, bid_travel_hours):
        travel_total = 0
        for travel in bid_travel_hours:
            quantity = travel.travel_hours_quantity
            hours = travel.travel_hours
            rate = travel.travel_rate
            travel_total += quantity * hours * rate.rate_amount
        return travel_total

    def get_travel_expenses(self, bid_travel_expenses):
        expense_total = 0
        for expense in bid_travel_expenses:
            quantity = expense.expense_quantity
            amount = expense.expense_amount
            expense_total += quantity * amount
        return expense_total

    def get_material_totals(self, bid_materials):
        material_total = 0
        for item in bid_materials:
            quantity = item.quantity
            # Get the UOM, which could be 'ea', 'ft', '100ea', '100ft', '1000ea', '1000ft'
            uom = item.unit_of_measure
            if any(x in uom for x in ['ea', 'ft']):
                uom = 1
            elif any(x in uom for x in ['100ea', '100ft']):
                uom = 100
            elif any(x in uom for x in ['1000ea', '1000ft']):
                uom = 1000
            else:
                uom = 1

            unit_price = item.unit_price

            material_total += quantity * uom * unit_price
        return material_total

    def get_equipment_totals(self, bid_equipment):
        equipment_total = 0
        for item in bid_equipment:
            quantity = item.quantity
            unit_price = item.unit_price
            equipment_total += quantity * unit_price
        return equipment_total
