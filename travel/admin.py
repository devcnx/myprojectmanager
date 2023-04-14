from django.contrib import admin
from .forms import TravelHoursForm, TravelExpenseForm
from .models import TravelHours, TravelExpense 


class TravelHoursAdmin(admin.ModelAdmin):
    form = TravelHoursForm


admin.site.register(TravelHours, TravelHoursAdmin)


class TravelExpenseAdmin(admin.ModelAdmin):
    form = TravelExpenseForm 


admin.site.register(TravelExpense, TravelExpenseAdmin)