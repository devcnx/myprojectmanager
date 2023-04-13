from django.db import models

class ResourceStatus(models.Model):
    resource_status_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Resource Status ID',
        db_column='resource_status_id',
    )
    resource_status = models.CharField(
        max_length=30,
        verbose_name='Resource Status',
        db_column='resource_status',
    )

    class Meta:
        db_table = 'resource_statuses'
        verbose_name = 'Resource Status'
        verbose_name_plural = 'Resource Statuses'
        ordering = ['resource_status']

    def __str__(self):
        return self.resource_status


class ResourceCompany(models.Model):
    resource_company_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Resource Company ID',
        db_column='resource_company_id',
    )
    resource_company = models.CharField(
        max_length=30,
        verbose_name='Resource Company',
        db_column='resource_company',
    )

    class Meta:
        db_table = 'resource_companies'
        verbose_name = 'Resource Company'
        verbose_name_plural = 'Resource Companies'
        ordering = ['resource_company']

    def __str__(self):
        return self.resource_company