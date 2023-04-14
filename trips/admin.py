from django.contrib import admin
from .forms import TripForm
from .models import Trip


class TripAdmin(admin.ModelAdmin):
    form = TripForm 
    list_display = ('trip_id', 'trip_number', 'trip_status', 'display_trip_date_details', 'trip_project_manager', 'trip_lead')
    filter_horizontal = ('trip_resources', 'trip_notes')
    search_fields = ('trip_number', 'trip_status', 'trip_project_manager', 'trip_lead', 'trip_resources')

    def display_trip_date_details(self, obj):
        start_year = obj.trip_start_date.year
        start_month = obj.trip_start_date.month
        start_day = obj.trip_start_date.day

        end_year = obj.trip_end_date.year
        end_month = obj.trip_end_date.month
        end_day = obj.trip_end_date.day

        start_hour = obj.trip_start_date.hour
        start_minutes = obj.trip_start_date.minute

        return f'{start_year}-{start_month}-{start_day} {start_hour}:{start_minutes} - {end_year}-{end_month}-{end_day}'

    display_trip_date_details.short_description = 'Trip Dates'

admin.site.register(Trip, TripAdmin)