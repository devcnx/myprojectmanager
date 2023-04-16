from django.core.exceptions import ValidationError
from django.db import models


class Rate(models.Model):
    RATE_TYPE_CHOICES = (
        ('Standard', 'Standard'),
        ('Blended', 'Blended'),
        ('Overtime', 'Overtime'),
        ('Double Time', 'Double Time'),
    )
    rate_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Rate Type ID',
        db_column='rate_id',
    )
    rate_type = models.CharField(
        max_length=50,
        choices=RATE_TYPE_CHOICES,
        verbose_name='Rate Type',
        db_column='rate_type',
        default='Standard',
    )
    rate_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Rate Amount',
        db_column='rate_amount',
    )

    class Meta:
        db_table = 'rates'
        verbose_name = 'Rate'
        verbose_name_plural = 'Rates'
        ordering = ['rate_id']

    def __str__(self):
        return f'{self.rate_amount:,.2f} Per Hour ({self.rate_type})'
