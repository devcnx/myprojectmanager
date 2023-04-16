from django.db import models


class VendorType(models.Model):
    vendor_type_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Vendor Type ID',
        db_column='vendor_type_id',
    )
    vendor_type = models.CharField(
        max_length=50,
        verbose_name='Vendor Type',
        db_column='vendor_type',
    )

    class Meta:
        db_table = 'vendor_types'
        verbose_name = 'Vendor Type'
        verbose_name_plural = 'Vendor Types'
        ordering = ['vendor_type']

    def __str__(self):
        return self.vendor_type


class Vendor(models.Model):
    vendor_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Vendor ID',
        db_column='vendor_id',
    )
    vendor_type = models.ForeignKey(
        VendorType,
        on_delete=models.CASCADE,
        verbose_name='Vendor Type',
        db_column='vendor_type_id',
    )
    vendor_name = models.CharField(
        max_length=50,
        verbose_name='Vendor Name',
        db_column='vendor_name',
    )

    class Meta:
        db_table = 'vendors'
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'
        ordering = ['vendor_name']

    def __str__(self):
        return self.vendor_name


class VendorContact(models.Model):
    vendor_contact_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Vendor Contact ID',
        db_column='vendor_contact_id',
    )
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        verbose_name='Vendor',
        db_column='vendor_id',
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name='First Name',
        db_column='first_name',
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Last Name',
        db_column='last_name',
        blank=True,
        null=True,
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
        max_length=255,
        verbose_name='Email',
        db_column='email',
    )

    class Meta:
        db_table = 'vendor_contacts'
        verbose_name = 'Vendor Contact'
        verbose_name_plural = 'Vendor Contacts'
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
