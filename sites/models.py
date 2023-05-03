from django.contrib.auth.models import User
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
        verbose_name='Site ID',
        db_column='site_id',
    )
    site_name = models.CharField(
        max_length=100,
        verbose_name='Site Name',
        db_column='site_name',
    )
    site_type = models.ForeignKey(
        SiteType,
        on_delete=models.CASCADE,
        verbose_name='Site Type',
        db_column='site_type_id',
        default=1,
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
    SITE_COUNTRY_CHOICES = (
        ('US', 'US'),
        ('CA', 'CA'),
    )
    country = models.CharField(
        max_length=50,
        verbose_name='Country',
        db_column='country',
        choices=SITE_COUNTRY_CHOICES,
        default='US',
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Phone',
        db_column='phone',
        blank=True,
        null=True,
    )
    added_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Added On',
        db_column='added_on',
    )
    added_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Added By',
        db_column='added_by',
        related_name='site_added_by',
        blank=True,
        null=True,
    )
    modified_on = models.DateTimeField(
        auto_now=True,
        verbose_name='Modified On',
        db_column='modified_on',
    )
    modified_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Modified By',
        db_column='modified_by',
        related_name='site_modified_by',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'sites'
        verbose_name = 'Site'
        verbose_name_plural = 'Sites'
        ordering = ['site_id']

    def __str__(self):
        return f'{self.site_id:04d} {self.site_name}'

    def save(self, user=None, *args, **kwargs):
        if user and not self.added_by:
            self.added_by = user
        if user and not self.modified_by:
            self.modified_by = user
        super(Site, self).save(*args, **kwargs)
