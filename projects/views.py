from django.shortcuts import redirect, render
from .forms import ProjectForm


def add_project(request):
    return render(request, 'projects/add_project.html')
