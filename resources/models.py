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