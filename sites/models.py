from django.db import models


class SiteType(models.Model):
    site_type_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Site Type ID',
        db_column='site_type_id',
    )
    site_type = models.CharField(
        max_length=50,
        verbose_name='Site Type',
        db_column='site_type',
    )

    class Meta:
        db_table = 'site_types'
        verbose_name = 'Site Type'
        verbose_name_plural = 'Site Types'
        ordering = ['site_type']

    def __str__(self):
        return self.site_type


class Site(models.Model):
    site_id = models.IntegerField(
        primary_key=True,
        editable=False,
        verbose_name='Site ID',
        db_column='site_id',
    )
    site_name = models.CharField(
        max_length=100,
        verbose_name='Site Name',
        db_column='site_name',
    )
    address = models.CharField(
        max_length=255,
        verbose_name='Address',
        db_column='address',
    )
    city = models.CharField(
        max_length=50,
        verbose_name='City',
        db_column='city',
    )
    state = models.CharField(
        max_length=2,
        verbose_name='State',
        db_column='state',
    )
    zip_code = models.CharField(
        max_length=10,
        verbose_name='Zip Code',
        db_column='zip_code',
    )
    country = models.CharField(
        max_length=50,
        verbose_name='Country',
        db_column='country',
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Phone',
        db_column='phone',
        blank=True,
        null=True,
    )
    site_type = models.ForeignKey(
        SiteType,
        on_delete=models.CASCADE,
        verbose_name='Site Type',
        db_column='site_type_id',
    )

    class Meta:
        db_table = 'sites'
        verbose_name = 'Site'
        verbose_name_plural = 'Sites'
        ordering = ['site_id']

    def __str__(self):
        return f'{self.site_id:04d} {self.site_name}'