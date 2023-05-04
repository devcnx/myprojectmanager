from customers.models import CustomerContact
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from sites.models import Site
from .forms import ProjectForm
from .models import Project


class AddProjectView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/add_project.html'
    success_url = reverse_lazy('bid:index')

    def get_form_kwargs(self):
        kwargs = super(AddProjectView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.last_updated_by = self.request.user
        response = super().form_valid(form)

        # Get the sites from the form.
        site_ids = self.request.POST.getlist('project_sites')

        # Associate the sites with the project.
        for site_id in site_ids:
            site = Site.objects.get(site_id=site_id)
            form.instance.project_sites.add(site)

        # Get the contacts from the form.
        contact_ids = self.request.POST.getlist('project_contacts')

        # Associate the contacts with the project.
        for contact_id in contact_ids:
            contact = CustomerContact.objects.get(
                customer_contact_id=contact_id)
            form.instance.project_contacts.add(contact)

        return response

    # Handle the case where the form is invalid
    def form_invalid(self, form):
        error_message = form.errors.as_text()
        return HttpResponse(error_message, status=400)


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_details.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.object
        context['project_contacts'] = self.get_project_contacts()
        context['project_sites'] = self.get_project_sites()
        return context

    def get_project_contacts(self):
        return self.object.project_contacts.all()

    def get_project_sites(self):
        return self.object.project_sites.all()


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/update_project.html'
