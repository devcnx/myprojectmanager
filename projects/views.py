from django.shortcuts import redirect, render
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from .forms import ProjectForm
from .models import Project


class AddProjectView(FormView):
    form_class = ProjectForm
    template_name = 'projects/add_project.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_form'] = ProjectForm()
        return context
