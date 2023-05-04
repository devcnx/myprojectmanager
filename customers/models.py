""" 
Customer Models 

Models :
    Customer - the customer
    CustomerContact - individual contacts for a given customer
"""

from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    """ 
    Represents a customer (as in a company).
    """
    customer_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Customer ID',
        db_column='customer_id',
    )
    customer_name = models.CharField(
        max_length=150,
        verbose_name='Customer Name',
        db_column='customer_name',
    )

    class Meta:
        db_table = 'customers'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['customer_name']

    def __str__(self):
        return self.customer_name


class CustomerContact(models.Model):
    """ 
    Represents a contact for a given customer.
    """
    customer_contact_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Customer Contact ID',
        db_column='customer_contact_id',
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name='Customer',
        db_column='customer_id',
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='First Name',
        db_column='first_name',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Last Name',
        db_column='last_name',
    )
    work_phone = models.CharField(
        max_length=20,
        verbose_name='Work Phone',
        db_column='work_phone',
        blank=True,
        null=True,
    )
    cell_phone = models.CharField(
        max_length=20,
        verbose_name='Cell Phone',
        db_column='cell_phone',
        blank=True,
        null=True,
    )
    email = models.EmailField(
        max_length=150,
        verbose_name='Email',
        db_column='email',
        blank=True,
        null=True,
    )
    added_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Added By',
        db_column='added_by',
        related_name='contact_added_by',
        blank=True,
        null=True,
    )
    added_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Added On',
        db_column='added_on',
    )
    last_updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Last Updated By',
        db_column='last_updated_by',
        related_name='contact_last_updated_by',
        blank=True,
        null=True,
    )
    last_updated_on = models.DateTimeField(
        auto_now=True,
        verbose_name='Last Updated On',
        db_column='last_updated_on',
    )

    class Meta:
        db_table = 'customer_contacts'
        verbose_name = 'Customer Contact'
        verbose_name_plural = 'Customer Contacts'
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, user=None, *args, **kwargs):
        """ 
        Override the save method to add the user to the added_by and last_updated_by fields if they are not already set.
        """
        if not self.added_by and user:
            self.added_by = user
        if not self.last_updated_by and user:
            self.last_updated_by = user
        super(CustomerContact, self).save(*args, **kwargs)
