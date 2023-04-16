from django.contrib import admin
from .forms import LaborHoursForm
from .models import LaborHours


class LaborHoursAdmin(admin.ModelAdmin):
    form = LaborHoursForm


admin.site.register(LaborHours, LaborHoursAdmin)
