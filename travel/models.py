from datetime import timedelta
from django.db import models
from notes.models import Note
from resources.models import Resource


class TravelHours(models.Model):
    TRAVEL_HOURS_CHOICES = (
        ('Home to Site', 'Home to Site'),
        ('Site to Site', 'Site to Site'),
        ('Site to Home', 'Site to Home'),
    )
    travel_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Travel ID',
        db_column='travel_id',
    )
    travel_type = models.CharField(
        max_length=50,
        choices=TRAVEL_HOURS_CHOICES,
        verbose_name='Travel Type',
        db_column='travel_type',
        default='Site to Site',
    )
    travel_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Travel Hours',
        db_column='travel_hours',
        default=0.00,
    )
    travel_date = models.DateField(
        verbose_name='Travel Date',
        db_column='travel_date',
    )
    week_ending = models.DateField(
        verbose_name='Week Ending',
        db_column='week_ending',
        blank=True,
    )
    travel_resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        verbose_name='Travel Resource',
        db_column='travel_resource',
    )
    travel_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Travel Created',
        db_column='travel_created',
    )
    travel_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Travel Updated',
        db_column='travel_updated',
    )
    travel_note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        verbose_name='Travel Note',
        db_column='travel_note',
        blank=True,
        null=True,
    )

    class Meta:
        db_table='travel'
        verbose_name='Travel'
        verbose_name_plural='Travel'
        ordering = ['-travel_created']

    def __str__(self):
        return f'W/E {self.week_ending} | {self.travel_resource} {self.travel_date} {self.travel_hours} {self.travel_type}'



    def save(self, *args, **kwargs):
        # Determine the week day based on the labor date
        week_day = self.travel_date.weekday() # 0 = Monday, 6 = Sunday
        # Find the number of days left until the end of the week (Sunday)
        days_to_end_of_week = 6 - week_day 
        # Add the number of days to the labor date to get the week ending date 
        self.week_ending = self.labor_date + timedelta(days=days_to_end_of_week)
        super().save(*args, **kwargs)


class TravelExpense(models.Model):
    EXPENSE_TYPE_CHOICES = (
        ('Airfare', 'Airfare'),
        ('Lodging', 'Lodging'),
        ('Food Per Diem', 'Food Per Diem'),
        ('Rental Car', 'Rental Car'),
        ('Mileage', 'Mileage'),
        ('Other', 'Other'),
    )
    travel_expense_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Travel Expense ID',
        db_column='travel_expense_id',
    )
    expense_type = models.CharField(
        max_length=50,
        choices=EXPENSE_TYPE_CHOICES,
        verbose_name='Expense Type',
        db_column='expense_type',
    )
    expense_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Expense Amount',
        db_column='expense_amount',
    )
    expense_date = models.DateField(
        verbose_name='Expense Date',
        db_column='expense_date',
    )
    week_ending = models.DateField(
        verbose_name='Week Ending',
        db_column='week_ending',
        blank=True,
    )
    expense_for = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        verbose_name='Expense For',
    )
    expense_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Expense Created',
        db_column='expense_created',
    )
    expense_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Expense Updated',
        db_column='expense_updated',
    )
    expense_note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        verbose_name='Expense Note',
        db_column='expense_note',
        blank=True,
        null=True,
    )

    class Meta:
        db_table='travel_expense'
        verbose_name='Travel Expense'
        verbose_name_plural='Travel Expenses'
        ordering = ['-expense_created']

    def __str__(self):
        return f'W/E {self.week_ending} | {self.expense_for} {self.expense_date} {self.expense_amount} {self.expense_type}'

    def save(self, *args, **kwargs):
        # Determine the week day based on the labor date
        week_day = self.expense_date.weekday()
        # Find the number of days left until the end of the week (Sunday)
        days_to_end_of_week = 6 - week_day
        # Add the number of days to the labor date to get the week ending date
        self.week_ending = self.expense_date + timedelta(days=days_to_end_of_week)
        super().save(*args, **kwargs)

