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