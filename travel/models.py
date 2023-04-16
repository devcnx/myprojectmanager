from datetime import timedelta
from django.db import models
from notes.models import Note
from rates.models import Rate
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
    travel_rate = models.ForeignKey(
        Rate,
        on_delete=models.CASCADE,
        verbose_name='Travel Rate',
        db_column='travel_rate',
        default=3,
    )
    travel_hours_quantity = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Travel Quantity',
        db_column='travel_quantity',
        default=0.00,
    )
    travel_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Travel Hours',
        db_column='travel_hours',
        default=0.00,
    )

    class Meta:
        db_table = 'travel'
        verbose_name = 'Travel'
        verbose_name_plural = 'Travel'
        ordering = ['-travel_id']

    def __str__(self):
        return f'{self.travel_type} - {self.travel_hours} Hours'

    # def save(self, *args, **kwargs):
    #     # Determine the week day based on the labor date
    #     week_day = self.travel_date.weekday() # 0 = Monday, 6 = Sunday
    #     # Find the number of days left until the end of the week (Sunday)
    #     days_to_end_of_week = 6 - week_day
    #     # Add the number of days to the labor date to get the week ending date
    #     self.week_ending = self.labor_date + timedelta(days=days_to_end_of_week)
    #     super().save(*args, **kwargs)


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
    expense_quantity = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Expense Quantity',
        db_column='expense_quantity',
        default=0.00,
    )
    expense_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Expense Amount',
        db_column='expense_amount',
        default=0.00,
    )
    # expense_date = models.DateField(
    #     verbose_name='Expense Date',
    #     db_column='expense_date',
    # )
    # week_ending = models.DateField(
    #     verbose_name='Week Ending',
    #     db_column='week_ending',
    #     blank=True,
    # )
    # expense_for = models.ForeignKey(
    #     Resource,
    #     on_delete=models.CASCADE,
    #     verbose_name='Expense For',
    # )
    # expense_created = models.DateTimeField(
    #     auto_now_add=True,
    #     verbose_name='Expense Created',
    #     db_column='expense_created',
    # )
    # expense_updated = models.DateTimeField(
    #     auto_now=True,
    #     verbose_name='Expense Updated',
    #     db_column='expense_updated',
    # )
    # expense_note = models.ForeignKey(
    #     Note,
    #     on_delete=models.CASCADE,
    #     verbose_name='Expense Note',
    #     db_column='expense_note',
    #     blank=True,
    #     null=True,
    # )

    class Meta:
        db_table = 'travel_expense'
        verbose_name = 'Travel Expense'
        verbose_name_plural = 'Travel Expenses'
        ordering = ['-travel_expense_id']

    def __str__(self):
        return f'{self.expense_type} - {self.expense_amount}'

    # def save(self, *args, **kwargs):
    #     # Determine the week day based on the labor date
    #     week_day = self.expense_date.weekday()
    #     # Find the number of days left until the end of the week (Sunday)
    #     days_to_end_of_week = 6 - week_day
    #     # Add the number of days to the labor date to get the week ending date
    #     self.week_ending = self.expense_date + timedelta(days=days_to_end_of_week)
    #     super().save(*args, **kwargs)
