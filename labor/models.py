from datetime import timedelta
from django.db import models
from notes.models import Note
from rates.models import Rate
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
    labor_rate = models.ForeignKey(
        Rate,
        on_delete=models.CASCADE,
        verbose_name='Labor Rate',
        db_column='labor_rate',
        default=2,
    )
    labor_hours_quantity = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Labor Quantity',
        db_column='labor_quantity',
        default=0.00,
    )
    labor_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Labor Hours',
        db_column='labor_hours',
        default=0.00,
    )

    class Meta:
        db_table = 'labor'
        verbose_name = 'Labor'
        verbose_name_plural = 'Labor'
        ordering = ['-labor_id']

    def __str__(self):
        return f'{self.labor_type} - {self.labor_hours} Hours'

    # def save(self, *args, **kwargs):
    #     # Determine the week day based on the labor date
    #     week_day = self.labor_date.weekday() # 0 = Monday, 6 = Sunday
    #     # Find the number of days left until the end of the week (Sunday)
    #     days_to_end_of_week = 6 - week_day
    #     # Add the number of days to the labor date to get the week ending date
    #     self.week_ending = self.labor_date + timedelta(days=days_to_end_of_week)
    #     super().save(*args, **kwargs)
