from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import SiteForm
from .models import Site


@login_required
def add_new_site(request):
    if request.method == 'POST':
        site_form = SiteForm(request.POST)
        if site_form.is_valid():
            site = site_form.save(commit=False)
            site.added_by = request.user
            site.modified_by = request.user
            site.save()
            return JsonResponse({
                'success': True,
                'site_id': site.pk,
                'site_name': site.site_name,
                'address': site.address,
                'city': site.city,
                'state': site.state,
                'zip_code': site.zip_code,
                'country': site.country,
                'phone': site.phone,
            })
        else:
            form_html = render_to_string(
                'sites/new_site_form.html',
                {'site_form': site_form},
                request=request,
            )
            return JsonResponse({
                'success': False,
                'form_html': form_html,
            })
    else:
        site_form = SiteForm()
        form_html = render_to_string(
            'sites/new_site_form.html',
            {'site_form': site_form},
            request=request,
        )
        return JsonResponse({
            'success': True,
            'form_html': form_html,
        })
