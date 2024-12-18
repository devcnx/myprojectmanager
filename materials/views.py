from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from .forms import MaterialForm
from .models import Material


class AddMaterialTemplateView(TemplateView):
    model = MaterialForm
    template_name = 'materials/add_material.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['add_material_form'] = MaterialForm()
        return context

    def post(self, request, *args, **kwargs):
        add_material_form = MaterialForm(request.POST)
        if add_material_form.is_valid():
            material = add_material_form.save(commit=False)
            # Check if a material with the same manufacturer and manufacturer number already exists
            existing_materials = Material.objects.filter(
                manufacturer_number=material.manufacturer_number)
            if existing_materials.exists():
                # Here, the material with the manufacturer/number already exists
                response_data = {
                    'error_message': 'Item Already Exists',
                    'status': 'error'}
                return JsonResponse(response_data)
            else:
                # Otherwise, save the material
                material.save()
                response_data = {
                    # 'material': material.material_id,
                    'description': material.description,
                    'manufacturer': material.manufacturer,
                    'manufacturer_number': material.manufacturer_number,
                    'status': 'success',
                }
                return JsonResponse(response_data)
        else:
            # The form isn't valid
            context = {'status': 'error',
                       'error_message': 'Confirm All Fields Are Completed and Try Again.'}

            return JsonResponse(context)
