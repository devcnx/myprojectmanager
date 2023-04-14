from django.contrib.auth.models import User
from django.db import models
from notes.models import Note
from resources.models import Resource


class Trip(models.Model):
    TRIP_STATUS_CHOICES = (
        ('Needs Scheduled', 'Needs Scheduled'),
        ('Scheduled', 'Scheduled'),
        ('In Progress', 'In Progress'),
        ('On Hold', 'On Hold'),
        ('Completed', 'Completed'),
        ('Completed - Needs Additional Trip', 'Completed - Needs Additional Trip'),
        ('Cancelled', 'Cancelled'),
    )
    trip_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Trip ID',
        db_column='trip_id',
    )
    trip_number = models.CharField(
        max_length=50,
        verbose_name='Trip Number',
        db_column='trip_number',
    )
    trip_status = models.CharField(
        max_length=50,
        choices=TRIP_STATUS_CHOICES,
        verbose_name='Trip Status',
        db_column='trip_status',
        default='Needs Scheduled',
    )
    trip_start_date = models.DateField(
        verbose_name='Trip Start Date',
        db_column='trip_start_date',
    )
    trip_start_time = models.TimeField(
        verbose_name='Trip Start Time',
        db_column='trip_start_time',
    )
    trip_end_date = models.DateField(
        verbose_name='Trip End Date',
        db_column='trip_end_date',
    )
    trip_end_time = models.TimeField(
        verbose_name='Trip End Time',
        db_column='trip_end_time',
    )
    trip_project_manager = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        verbose_name='Trip Project Manager',
        db_column='trip_project_manager',
        limit_choices_to={'is_project_manager': True},
        related_name='trip_project_manager',
    )
    trip_lead = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        verbose_name='Trip Lead',
        db_column='trip_lead',
        related_name='trip_lead',
    )
    trip_resources = models.ManyToManyField(
        Resource,
        verbose_name='Trip Resources',
        db_column='trip_resources',
        blank=True,
        related_name='trip_resource',
    )
    trip_notes = models.ManyToManyField(
        Note,
        verbose_name='Trip Notes',
        db_column='trip_notes',
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created On',
        db_column='created_on',
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Created By',
        db_column='created_by',
        related_name='trip_created_by',
    )
    updated_on = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated On',
        db_column='updated_on',
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Updated By',
        db_column='updated_by',
        related_name='trip_updated_by',
    )

    class Meta:
        db_table = 'trips'
        verbose_name = 'Trip'
        verbose_name_plural = 'Trips'
        ordering = ['-trip_start_date']

    def __str__(self):
        return self.trip_number



