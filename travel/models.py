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

    class Meta:
        db_table = 'travel_expense'
        verbose_name = 'Travel Expense'
        verbose_name_plural = 'Travel Expenses'
        ordering = ['-travel_expense_id']

    def __str__(self):
        return f'{self.expense_type} - {self.expense_amount}'
