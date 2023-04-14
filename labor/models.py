from datetime import timedelta
from django.db import models
from notes.models import Note 
from resources.models import Resource

class LaborHours(models.Model):
    LABOR_HOURS_CHOICES = (
        ('Office', 'Office'),
        ('Project', 'Project'),
        ('Training', 'Training'),
        ('Partner', 'Partner'),
        ('Site Survey', 'Site Survey'),
        ('Emergency', 'Emergency'),
        ('Project Management', 'Project Management'),
    )
    labor_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Labor ID',
        db_column='labor_id',
    )
    labor_type = models.CharField(
        max_length=50,
        choices=LABOR_HOURS_CHOICES,
        verbose_name='Labor Type',
        db_column='labor_type',
        default='Project',
    )
    labor_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Labor Hours',
        db_column='labor_hours',
        default=0.00,
    )
    labor_date = models.DateField(
        verbose_name='Labor Date',
        db_column='labor_date',
    )
    week_ending = models.DateField(
        verbose_name='Week Ending',
        db_column='week_ending',
        blank=True,
    )

    labor_resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        verbose_name='Labor Resource',
        db_column='labor_resource',
    )
    labor_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Labor Created',
        db_column='labor_created',
    )
    labor_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Labor Updated',
        db_column='labor_updated',
    )
    labor_note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        verbose_name='Labor Notes',
        db_column='labor_notes',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'labor'
        verbose_name = 'Labor'
        verbose_name_plural = 'Labor'
        ordering = ['-labor_created']

    def __str__(self):
        return f'W/E {self.week_ending} | {self.labor_resource} {self.labor_date} {self.labor_hours} {self.labor_type}'

    def save(self, *args, **kwargs):
        # Determine the week day based on the labor date
        week_day = self.labor_date.weekday() # 0 = Monday, 6 = Sunday
        # Find the number of days left until the end of the week (Sunday)
        days_to_end_of_week = 6 - week_day 
        # Add the number of days to the labor date to get the week ending date 
        self.week_ending = self.labor_date + timedelta(days=days_to_end_of_week)
        super().save(*args, **kwargs)
