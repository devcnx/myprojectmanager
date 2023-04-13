from django.contrib import admin
from .forms import TravelHoursForm
from .models import TravelHours


class TravelHoursAdmin(admin.ModelAdmin):
    form = TravelHoursForm


admin.site.register(TravelHours, TravelHoursAdmin)
