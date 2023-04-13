from django.db import models


class Customer(models.Model):
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
    )

    class Meta:
        db_table = 'customer_contacts'
        verbose_name = 'Customer Contact'
        verbose_name_plural = 'Customer Contacts'
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'